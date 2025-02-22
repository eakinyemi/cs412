"""
URL routing for the mini_fb application.
"""

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView

app_name = 'mini_fb'

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
]
