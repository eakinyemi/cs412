"""
View definitions for the mini_fb application.
"""


from django.views.generic import DetailView, ListView, CreateView
from django.shortcuts import render
from django.urls import reverse
from .models import StatusMessage, Profile
from .forms import CreateStatusMessageForm

# Create your views here.
class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = "profiles"
    def get_queryset(self):
        return Profile.objects.all()
    """
    Displays all user profiles in a list view.
    Template: show_all_profiles.html
    Context:
        object_list: List of all Profile objects.
    """


class ShowProfilePageView(DetailView):
    '''Show details of a single profile using its primary key (pk).'''
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        '''Retrieve the profile by pk. If not found, return logged-in user's profile.'''
        pk = self.kwargs.get("pk")
        if pk:
            return Profile.objects.get(pk=pk)
        return self.request.user.profile
    
class CreateStatusMessageView(CreateView):
    """A view to create a new StatusMessage and associate it with a Profile."""
    model = StatusMessage
    form_class = CreateStatusMessageForm  # Using our new form
    template_name = "mini_fb/create_status_form.html"

    def form_valid(self, form):
        """Attach the correct Profile to the StatusMessage before saving."""
        profile_id = self.kwargs['pk']  # Get the profile's ID from the URL
        profile = Profile.objects.filter(pk=profile_id).first()  # Fetch Profile 

        if profile:  # Ensure the profile exists
            form.instance.profile = profile  # Attach it to the StatusMessage
            return super().form_valid(form)
        else:
            # If no profile is found, redirect back to the home page or profile list
            return render(self.request, "mini_fb/error.html", {"message": "Profile not found."})

    def get_success_url(self):
        """Redirect back to the Profile page after posting a status message."""
        return reverse('mini_fb:show_profile', args=[self.kwargs['pk']])