from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model

import misaka

from groups.models import Group

# Create your models here.
# Grabbing the User Model instance, active in the current session.
User = get_user_model()

class Post(models.Model):
    """A Model for Post table.\n
    user(User): User instance of user who wrote post.
    created_on(DateTime): Date & time of creation.
    message(str): The Post.
    group(Group): The group to which the post belongs.
    """
    user            = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    created_on      = models.DateTimeField(auto_now=True)
    message         = models.TextField()
    message_html    = models.TextField(editable=False)
    likes           = models.ManyToManyField(User, related_name='likes', blank=True)
    group           = models.ForeignKey(Group, related_name='groupposts', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username':self.user.username,
                                               'pk': self.pk})

    class Meta:
        ordering = ['-created_on']
        unique_together = ['user', 'message']


class Comments(models.Model):
    """Test class for comments."""

    post        = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author      = models.ForeignKey(User, editable=False, related_name='my_comments', on_delete=models.CASCADE)
    text        = models.TextField(max_length=200)
    created_on  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['created_on']

    