"""
View definitions for the mini_fb application.
"""

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
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
        if "user_form" not in context:
            context["user_form"] = UserCreationForm()
        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            # Save the user
            user = user_form.save()

            # Attach user to profile and save it
            form.instance.user = user
            self.object = form.save()

            # Optionally, log in the user
            login(self.request, user)

            return reverse("mini_fb:show_profile")
        else:
            return self.render_to_response(
                self.get_context_data(form=form, user_form=user_form)
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
    
    
class AddFriendView(LoginRequiredMixin, View):
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def get_object(self):
        return self.request.user.profile
    def dispatch(self, request, *args, **kwargs):
        other_pk = self.kwargs.get("other_pk")
        try:
            other = Profile.objects.get(pk=other_pk)
            profile = request.user.profile
            profile.add_friend(other)
        except Profile.DoesNotExist:
            pass  # You could add a message here if you want

        return redirect("mini_fb:show_profile")
    
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


