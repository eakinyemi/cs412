from django import forms
from .models import Profile, StatusMessage

class CreateStatusMessageForm(forms.ModelForm):
    """A form for creating status messages."""

    class Meta:
        model = StatusMessage
        fields = ['message']  # Only let users input the message
