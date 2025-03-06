"""
Defines the Profile model for the mini_fb application, representing user profiles.
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    """
    Model representing a Facebook-like user profile.
    
    Attributes:
        first_name (str): User's first name.
        last_name (str): User's last name.
        city (str): User's city of residence.
        email (str): User's email address.
        profile_image_url (str): URL to the user's profile image.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile",  default=1)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    profile_image_url =  models.URLField(blank=True, null=True)
    

    def __str__(self):
        """Return a string representation of the profile."""
        return f"{self.first_name} {self.last_name}"
    def get_all_status_messages(self):
        """Return all status messages associated with the profile."""
        return StatusMessage.objects.filter(profile=self)
    def get_absolute_url(self):
        """Return the URL to access a particular profile instance."""
        return reverse('mini_fb:show_profile', kwargs={'pk': self.profile.pk})

class StatusMessage(models.Model):
    """
        Model representing a user's status message.
    
    Attributes:
        profile (Profile): Profile associated with the status message.
        message (str): User's status message.
        timestamp (datetime): Date and time the status message was created.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message  = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('mini_fb:show_profile', kwargs={self.profile.pk})

    def __str__(self):
        """Return a string representation of the status message."""
        return f"{self.profile}: {self.message}"