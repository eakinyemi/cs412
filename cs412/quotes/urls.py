from django.urls import path
from django.conf import settings
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.quote, name='base'),
    path('quote/', views.quote, name='quote'),
    path('show_all/', views.show_all, name='show_all'),
    path('about/', views.about, name='about'),
]
 