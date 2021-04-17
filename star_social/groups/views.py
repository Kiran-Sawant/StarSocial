from django.shortcuts import render
from django.views import generic as gen
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin)
from django.urls import (reverse, reverse_lazy)
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db import IntegrityError

from . import models
from posts.models import Post

# Create your views here.
class CreateGroup(LoginRequiredMixin, gen.CreateView):
    """CBV for creating a Group instance."""

    model = models.Group
    fields = ('name', 'description')

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)

class SingleGroup(gen.DetailView, MultipleObjectMixin):
    """Detail view of a single Group instance."""

    model = models.Group

    paginate_by = 5

    def get_context_data(self, **kwargs):
        object_list = Post.objects.filter(group=self.object)
        context = super(SingleGroup, self).get_context_data(object_list=object_list, **kwargs)
        return context


class ListGroup(gen.ListView):
    """ListView for a list of all Group instances."""

    model = models.Group

    paginate_by = 6


class JoinGroup(LoginRequiredMixin, gen.RedirectView):
    """Redirect view for carring out certain operations before joining a Group"""
    
    def get_redirect_url(self, *args, **kwargs):
        """RedirectView method to pass a URL to redirect the user"""

        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, *args, **kwargs):
        """Overriding Redirect view method.\n
        Things to do on a get request on JoinGroup view"""

        # Creating a Group instance
        group = get_object_or_404(models.Group, slug=self.kwargs.get('slug'))

        try:    # try creating a GroupMember instance from active User.
            models.GroupMember.objects.create(user=self.request.user, group=group)
        except IntegrityError:      # If active User is already a Member.
            messages.warning(self.request, 'You are already a member of this group!')
        else:
            messages.success(self.request, 'You are now a member of this group!')

        return super().get(self.request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, gen.RedirectView):
    """RedirectView for Leaving a Group"""
    
    def get_redirect_url(self, *args, **kwargs):
        """RedirectView method to pass a URL to redirect the user"""
        
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):

        try:
            membership = models.GroupMember.objects.filter(
                user = self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request, 'Sorry you are not in this group!')
        else:
            membership.delete()
            messages.success(self.request, 'You have left the Group!')

        return super().get(self.request, *args, **kwargs)


class DeleteGroup(LoginRequiredMixin, gen.DeleteView):

    model = models.Group
    success_url = reverse_lazy("groups:all")

    def delete(self, *args, **kwargs):
        """overriding Method for deleting instances."""

        messages.success(self.request, "Group Deleted")
        return super().delete(*args, **kwargs)