from django.shortcuts import (render, get_object_or_404, redirect)
from django.urls import reverse_lazy, reverse
from django.http import Http404
from django.views import generic as gen
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from braces.views import SelectRelatedMixin

from accounts.models import User 
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


class PostDetail(SelectRelatedMixin, gen.DetailView, MultipleObjectMixin):

    model = models.Post
    select_related = ('user', 'group')

    paginate_by = 8

    def get_context_data(self, **kwargs):
        comment_list = models.Comments.objects.filter(post=self.object)
        context = super(PostDetail, self).get_context_data(object_list=comment_list, **kwargs)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

    def get_like_url(self):
        return reverse('posts:like-toggle', kwargs={'username':self.kwargs.get('username'), 
                                                    'pk':self.kwargs.get('pk')})


class PostLikeToggleRedirect(LoginRequiredMixin, gen.RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):

        user_name     = self.kwargs.get('username')  # post author name(User)
        # print(f"{user_name}: type {type(user_name)}")
        user          = get_object_or_404(User, username=user_name)     # post author(User)
        # print(f"{user}: type {type(user)}")
        pk            = self.kwargs.get('pk')        # post pk
        # print(pk)

        post_obj = get_object_or_404(models.Post, user=user, pk=pk)
        # print(post_obj)
        url_ = post_obj.get_absolute_url()
        user = self.request.user                # active user

        if user.is_authenticated:               # If user is logged in
            if user in post_obj.likes.all():    # if user has already liked post
                post_obj.likes.remove(user)
            else:                               # If user hasn't liked post
                post_obj.likes.add(user)
        else:                                   # user not logged-in
            redirect('login')

        return url_

class CreatePost(LoginRequiredMixin, SelectRelatedMixin, gen.CreateView):
    
    select_related = (u'author', u'group')
    model = models.Post
    fields = ('message', 'group')

    def form_valid(self, form):
        """Overriding superclass method, to connect the active user
        with the user field in the Post Model before saving."""

        self.object = form.save(commit=False)
        print(self.object.message)
        # print(self.object.user.username)
        self.object.user = self.request.user       # connecting the User with the Post
        print(self.object.user.username)
        self.object.save()
        return super().form_valid(form)


class UpdatePost(LoginRequiredMixin, gen.UpdateView):

    model = models.Post
    fields = ('message', 'group')

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


#######################################################
#           Based views for Comments                  #
#######################################################
@login_required
def add_commment(request, pk):
    """A view for adding comment to a post."""

    post = get_object_or_404(models.Post, pk=pk)

    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post             # inserting post in coments post field
            comment.author = request.user
            comment.save()
            return redirect(post, permanent=True)
        else:
            messages.success(request, "Invalid fields!")
    else:
        form = forms.CommentForm()

    return render(request, 'posts/comment_form.html', {'form': form, 'post':post})

@login_required
def delete_comment(request, pk):
    """A view to delete a comment"""

    comment = get_object_or_404(models.Comments, pk=pk)
    post = get_object_or_404(models.Post, pk=comment.post.pk)
   
    comment.delete()
    return redirect(post, permanent=True)