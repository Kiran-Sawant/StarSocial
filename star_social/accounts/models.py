from django.db import models
from django.contrib import auth

# Create your models here.
class User(auth.models.User, auth.models.PermissionsMixin):
    """A User model based directly on the django User model."""

    def __str__(self):
        return f"@{self.username}"