from django.urls import path
from . import views

urlpatterns = [
    path('reporter/', views.reporter_dashboard, name='reporter_dashboard'),
    path('collector/', views.collector_dashboard, name='collector_dashboard'),
    path('admin_dash/', views.admin_dashboard, name='admin_dashboard'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
