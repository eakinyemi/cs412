"""
Defines the Profile model for the mini_fb application, representing user profiles.
"""

from django.db import models

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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    email = models.EmailField()
    profile_image_url = models.URLField()

    def __str__(self):
        """Return a string representation of the profile."""
        return f"{self.first_name} {self.last_name}"