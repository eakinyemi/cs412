"""
View definitions for the mini_fb application.
"""

from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.urls import reverse
from .models import Profile, StatusMessage, Image, StatusImage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm

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

        # Handle image uploads
        files = self.request.FILES.getlist('files')
        for file in files:
            img = Image(profile=profile, image_file=file)
            img.save()
            status_img = StatusImage(status_message=sm, image=img)
            status_img.save()

        return super().form_valid(form)

    

    def get_context_data(self, **kwargs):
        """Ensure profile context is available in the template."""
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(pk=self.kwargs['pk'])  # Fetch the profile
        return context

    def get_success_url(self):
        """Redirect back to the Profile page after posting a status message."""
        return reverse('mini_fb:show_profile', kwargs={'pk': self.kwargs['pk']})
    
class UpdateProfileView(UpdateView):
    """View to update an existing Profile."""
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_success_url(self):
        return reverse('mini_fb:show_profile', kwargs={'pk': self.object.pk})
class UpdateStatusMessageView(UpdateView):
    """View to update a StatusMessage."""
    model = StatusMessage
    fields = ['message']
    template_name = "mini_fb/update_status_form.html"

    def get_success_url(self):
        return reverse('mini_fb:show_profile', kwargs={'pk': self.object.profile.pk})
class DeleteStatusMessageView(DeleteView):
    """View to delete a StatusMessage."""
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"

    def get_success_url(self):
        return reverse('mini_fb:show_profile', kwargs={'pk': self.object.profile.pk})
    
class AddFriendView(View):
    """Adds a friend and redirects to profile page."""
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        other_pk = self.kwargs.get("other_pk")
        profile = Profile.objects.get(pk=pk)
        other = Profile.objects.get(pk=other_pk)

        profile.add_friend(other)
        return reverse('mini_fb:show_profile', kwargs={'pk': self.object.profile.pk})
    
class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['suggestions'] = profile.get_friend_suggestions()
        return context
class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context["feed"] = profile.get_news_feed()
        return context
