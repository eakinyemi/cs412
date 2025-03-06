"""
URL routing for the mini_fb application.
"""

from django.urls import path
from .views import * #ShowAllProfilesView, ShowProfilePageView, CreateStatusMessageView

app_name = "mini_fb"

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profiles/', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
    path('profile/<int:pk>/create_status_form/', CreateStatusMessageView.as_view(), name="create_status_form"),

]
