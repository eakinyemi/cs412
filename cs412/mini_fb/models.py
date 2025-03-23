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
    
    def get_friends(self):
        """Return a list of Profile objects that are friends with this profile."""
        # Friends where this profile is profile1
        friends1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        # Friends where this profile is profile2
        friends2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)
        # Combine both sets
        friend_ids = list(friends1) + list(friends2)
        return Profile.objects.filter(id__in=friend_ids)
    def add_friend(self, other):
        """Add a friend if not already friends and not self."""
        if self == other:
            return  # Prevent self-friendship

        # Check if a friendship already exists
        if Friend.objects.filter(profile1=self, profile2=other).exists() or Friend.objects.filter(profile1=other, profile2=self).exists():
            return  # Already friends

        # Create the friendship
        Friend.objects.create(profile1=self, profile2=other)

    def get_friend_suggestions(self):
        """Suggest profiles that are not already friends and not self."""
        all_profiles = Profile.objects.exclude(id=self.id)
        current_friends = self.get_friends()
        return all_profiles.exclude(id__in=current_friends.values_list('id', flat=True))


    def get_all_status_messages(self):
        return StatusMessage.objects.filter(profile=self)
    
    def get_news_feed(self):
        """Return all status messages for this profile and its friends."""
        friend_ids = self.get_friends().values_list('id', flat=True)
        all_ids = list(friend_ids) + [self.id]
        return StatusMessage.objects.filter(profile__id__in=all_ids).order_by('-timestamp')

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
    
class Friend(models.Model):
    """Model representing a friendship between two profiles."""
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"
