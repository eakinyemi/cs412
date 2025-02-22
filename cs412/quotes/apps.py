"""
Configuration for the mini_fb Django application.
"""
from django.apps import AppConfig

class MiniFbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cs412.mini_fb'  # Specifies the full Python path to the application