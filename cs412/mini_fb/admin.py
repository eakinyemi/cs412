"""
Admin configuration for the mini_fb application.
Registers the Profile model to make it accessible in the Django admin interface.
"""
from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User
from .models import StatusMessage

# Register your models here.

admin.site.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'email')

"""Profile.objects.create(
    user=user, first_name="Evan", last_name="Akinyemi", city="Boston", email="evanakinyemi@gmail.com", image_url="https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
    )
"""
admin.site.register(StatusMessage)