"""
Defines the Profile model for the mini_fb application, representing user profiles.
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Profile(models.Model):
    """Model representing a Facebook-like user profile."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", default=1)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    profile_image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_all_status_messages(self):
        return StatusMessage.objects.filter(profile=self)

    def get_absolute_url(self):
        return reverse('mini_fb:show_profile', kwargs={'pk': self.pk})


class StatusMessage(models.Model):
    """Model representing a user's status message."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile}: {self.message}"
    
    def get_images(self):
        """Retrieve all images associated with this StatusMessage."""
        return Image.objects.filter(statusimage__status_message=self)

    def get_absolute_url(self):
        return reverse('mini_fb:show_profile', kwargs={'pk': self.profile.pk})


class Image(models.Model):
    """Model representing an image uploaded by a user."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='uploads/')
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Image uploaded by {self.profile}"


class StatusImage(models.Model):
    """Model to associate an image with a status message."""
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for StatusMessage {self.status_message.pk}"
