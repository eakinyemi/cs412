"""
View definitions for the mini_fb application.
"""

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.urls import reverse
from .models import Profile, StatusMessage, Image, StatusImage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login # NEW
# Create your views here.
class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = "profiles"

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            print(f'ShowAllProfilesView.dispatch(): request.user = {request.user}')
        else:
            print(f'ShowAllProfilesView.dispatch(): not logged in')

        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return Profile.objects.all()
    """
    Displays all user profiles in a list view.
    Template: show_all_profiles.html
    Context:
        object_list: List of all Profile objects.
    """


class ShowProfilePageView(DetailView, LoginRequiredMixin):
    '''Show details of a single profile using its primary key (pk).'''
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        if "pk" in self.kwargs:
            return Profile.objects.get(pk=self.kwargs["pk"])
        return self.request.user.profile
    
class CreateProfileView(CreateView):
    model = Profile
    template_name = "mini_fb/create_profile.html"
    form_class = CreateProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_form"] = UserCreationForm(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):
        profile_form = self.get_form()
        user_form = UserCreationForm(self.request.POST)

        if profile_form.is_valid() and user_form.is_valid():
            # Create user
            user = user_form.save()

            # Create profile, link to user
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Manually assign self.object for CreateView internals
            self.object = profile

            return super().form_valid(profile_form)
        
        return self.render_to_response(
            self.get_context_data(form=profile_form, user_form=user_form)
        )

        

    def get_success_url(self):
        return reverse("mini_fb:login")
    
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.request.user.profile
        return context

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        sm = form.save()

        files = self.request.FILES.getlist('files')
        for file in files:
            img = Image(profile=self.request.user.profile, image_file=file)
            img.save()
            StatusImage.objects.create(status_message=sm, image=img)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("mini_fb:show_profile")

    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"
    context_object_name = "profile"

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        return reverse("mini_fb:show_profile")
class UpdateStatusMessageView(UpdateView, LoginRequiredMixin):
    """View to update a StatusMessage."""
    model = StatusMessage
    fields = ['message']
    template_name = "mini_fb/update_status_form.html"

    def get_object(self):
        return self.request.user.profile

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 


    def get_success_url(self):
        return reverse("mini_fb:show_profile")
class DeleteStatusMessageView(DeleteView, LoginRequiredMixin):
    """View to delete a StatusMessage."""
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    def get_object(self):
        return self.request.user.profile

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 

    def get_success_url(self):
        return reverse("mini_fb:show_profile")
    
class AddFriendView(View, LoginRequiredMixin):
    """Adds a friend and redirects to profile page."""
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def get_object(self):
        return self.request.user.profile
    
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        other_pk = self.kwargs.get("other_pk")
        profile = Profile.objects.get(pk=pk)
        other = Profile.objects.get(pk=other_pk)

        profile.add_friend(other)
        return reverse("mini_fb:show_profile")
    
class ShowFriendSuggestionsView(DetailView, LoginRequiredMixin):
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def get_object(self):
        return self.request.user.profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['suggestions'] = profile.get_friend_suggestions()
        return context
class ShowNewsFeedView(DetailView, LoginRequiredMixin):
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"

    def get_object(self):
        return self.request.user.profile

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context["feed"] = profile.get_news_feed()
        return context


class UserRegistrationView(CreateView):
    '''A view to show/process the registration form to create a new User.'''

    template_name = 'mini_fb/register.html'
    form_class = UserCreationForm
    model = User
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # auto login after register
        return reverse("mini_fb:create_profile")  # route them to create their profile

    def get_success_url(self):
        '''The URL to redirect to after creating a new User.'''
        return reverse('login')