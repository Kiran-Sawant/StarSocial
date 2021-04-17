from django.contrib import admin
from .models import Post, Comments

# Register your models here.
admin.site.register(Comments)
admin.site.register(Post)