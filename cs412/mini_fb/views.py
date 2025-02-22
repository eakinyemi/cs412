"""
View definitions for the mini_fb application.
"""

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

# Create your views here.
class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    """
    Displays all user profiles in a list view.
    Template: show_all_profiles.html
    Context:
        object_list: List of all Profile objects.
    """

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile_page.html'
    """
    Displays the details of a single user profile.
    Template: show_profile.html
    Context:
        object: Profile instance specified by pk.
    """