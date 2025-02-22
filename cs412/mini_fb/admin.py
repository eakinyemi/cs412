"""
Admin configuration for the mini_fb application.
Registers the Profile model to make it accessible in the Django admin interface.
"""
from django.contrib import admin
from .models import Profile

# Register your models here.

admin.site.register(Profile)