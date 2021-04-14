from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic as gen
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from braces.views import SelectRelatedMixin

from . import models
from . import forms

# Create your views here.
# User active in the given session.
User = get_user_model()

class PostList(SelectRelatedMixin, gen.ListView):
    """A view for posts in a Group"""
    model = models.Post
    select_related = ('user', 'group')

    paginate_by = 6

class UserPosts(gen.ListView):
    """A view for list of posts by a User."""
    model = models.Post
    template_name = 'posts/user_post_list.html'

    paginate_by = 6

    def get_queryset(self):
        """Get a query set of posts where user in Post is current User"""
        try:
            # Fetch the posts by the active User, kwargs passed from urls.py
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user

        return context


class PostDetail(SelectRelatedMixin, gen.DetailView):

    model = models.Post
    select_related = ('user', 'group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, gen.CreateView):
    
    model = models.Post
    select_related = (u'user', u'group')
    fields = ('message', 'group')

    def form_valid(self, form):
        """Overriding superclass method, to connect the active user
        with the user field in the Post Model before saving."""

        self.object = form.save(commit=False)
        self.object.user = self.request.user       # connecting the User with the Post
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, gen.DeleteView):

    model = models.Post
    select_related = ('user', 'group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        """List of posts by this user"""
        queryset = super().get_queryset()
        # SELECT * FROM Post WHERE user_id == self.request.user.id
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args , **kwargs):
        """Method for deleting an instance of Model"""

        messages.success(self.request, 'Post Deleted!')
        return super().delete(*args, **kwargs)      # calling delete method


