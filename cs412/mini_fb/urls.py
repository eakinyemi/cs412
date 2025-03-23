"""
URL routing for the mini_fb application.
"""

from django.urls import path
from .views import * # ShowAllProfilesView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView

app_name = "mini_fb"

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profiles/', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>/create_status_form/', CreateStatusMessageView.as_view(), name="create_status_form"),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"),
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name="update_status"),
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name="delete_status"),
    path('profile/<int:pk>/add_friend/<int:other_pk>/', AddFriendView.as_view(), name="add_friend"),
    path('profile/<int:pk>/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name="friend_suggestions"),
    path('profile/<int:pk>/news_feed/', ShowNewsFeedView.as_view(), name="news_feed"),

]
