from django.urls import path
from . import views

app_name = 'voter_analytics'


urlpatterns = [
    path('', views.VoterListView.as_view(), name='base'),
    path('voters/', views.VoterListView.as_view(), name='voter_list'),
    path('voter/<int:pk>', views.VoterDetailView.as_view(), name='voter_detail'),
    path('graphs/', views.VoterGraphView.as_view(), name='graphs'),

]