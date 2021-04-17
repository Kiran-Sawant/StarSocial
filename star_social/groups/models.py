from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django import template
from django.urls import reverse

import misaka

# Create your models here.
# getting objects from the user that is currently active in this session (reating user model).
User = get_user_model()

# Library instance for registering template filters & template tags.
register = template.Library()

class Group(models.Model):
    """A Model for Group table.

    name(str): Name of the group (should be unique)\n
    description(str): Description of the group."""

    name             = models.CharField(max_length=255, unique=True)
    slug             = models.SlugField(allow_unicode=True, unique=True)
    description      = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members          = models.ManyToManyField(User, through='GroupMember')               # One group can hav many users & vice-versa.
    created_by       = models.ForeignKey(User, related_name='admin', on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)      # Converting group name to slug.
        self.description_html = misaka.html(self.description)

        super().save(*args, **kwargs)

    def get_absolute_url(self):

        return reverse('groups:single', kwargs={'slug':self.slug})


class GroupMember(models.Model):
    """A Model for defining the many to many relation between groups and users.
    One user can be in many groups & one group can have many users."""

    group = models.ForeignKey(Group, related_name='memberships', on_delete=models.CASCADE)
    user  = models.ForeignKey(User, related_name='user_group', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        """Defining the relation between User Model and Group Model,
        many to many relations requires an intermediary junction table,
        GroupMember is that junction table, line below defines it to Django ORM."""
        unique_together = ('group', 'user')
