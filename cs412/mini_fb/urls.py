"""
URL routing for the mini_fb application.
"""

from django.urls import path
from .views import * # ShowAllProfilesView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView

from django.contrib.auth import views as auth_views

app_name = "mini_fb"

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profiles/', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/', ShowProfilePageView.as_view(), name='show_profile'),
    path("profile/<int:pk>/", ShowProfilePageView.as_view(), name="show_profile"),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('profile/create_status_form/', CreateStatusMessageView.as_view(), name="create_status_form"),
    path('profile/update', UpdateProfileView.as_view(), name="update_profile"),
    path("status/<int:pk>/update/", UpdateStatusMessageView.as_view(), name="update_status"),
    path("status/<int:pk>/delete/", DeleteStatusMessageView.as_view(), name="delete_status"),
    path('profile/add_friend/<int:other_pk>/', AddFriendView.as_view(), name="add_friend"),
    path('profile/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name="friend_suggestions"),
    path('profile/news_feed/', ShowNewsFeedView.as_view(), name="news_feed"),
  

    # authorization-related paths
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path("logout/", auth_views.LogoutView.as_view(template_name="mini_fb/logged_out.html"), name="logout"),
]
