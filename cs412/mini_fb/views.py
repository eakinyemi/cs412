"""
View definitions for the mini_fb application.
"""


from django.views.generic import DetailView, ListView, CreateView
from django.shortcuts import render
from django.urls import reverse
from .models import Profile
from .forms import CreateProfileForm, CreateStatusMessageForm

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
    
class CreateProfileView(CreateView):
    """View to create a new Profile."""
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile.html'
    
    def form_valid(self, form):
        """Set the user automatically before saving."""
        form.instance.user = self.request.user  # Assign logged-in user
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the new profile page after creation."""
        return reverse('mini_fb:show_profile', kwargs={'pk': self.object.pk})
    
class CreateStatusMessageView(CreateView):
    """A view to create a new StatusMessage and associate it with a Profile."""
    form_class = CreateStatusMessageForm  # Using form
    template_name = "mini_fb/create_status_form.html"

    def form_valid(self, form):
        """Attach the correct Profile to the StatusMessage before saving."""
        profile_id = self.kwargs['pk']  # Get the profile's ID from the URL
        profile = Profile.objects.get(pk=profile_id)  # Fetch Profile instance

        form.instance.profile = profile  # Attach it to the StatusMessage
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Ensure profile context is available in the template."""
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(pk=self.kwargs['pk'])  # Fetch the profile
        return context

    def get_success_url(self):
        """Redirect back to the Profile page after posting a status message."""
        return reverse('mini_fb:show_profile', kwargs={'pk': self.kwargs['pk']})