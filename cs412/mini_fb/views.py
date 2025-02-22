from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

# Create your views here.
class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile_page.html'