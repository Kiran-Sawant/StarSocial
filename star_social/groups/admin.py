from django.contrib import admin
from . import models

# Register your models here.

class GroupMembersInline(admin.TabularInline):
    """A Model for defining relation between GroupMember and Group."""
    model = models.GroupMember

admin.site.register(models.Group)