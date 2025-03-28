from django import forms
from .models import Profile, StatusMessage


class CreateProfileForm(forms.ModelForm):
    """A form to create a new Profile."""
    
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url']  # users input these fields

class CreateStatusMessageForm(forms.ModelForm):
    """A form for creating status messages."""

    class Meta:
        model = StatusMessage
        fields = ['message']  # Only let users input the message
class UpdateProfileForm(forms.ModelForm):
    """Form for updating a profile."""
    
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url']
