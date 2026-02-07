"""
Configuration des URLs pour l'application home.

Ce module définit les routes pour l'accueil, l'enregistrement,
la connexion et la déconnexion.
"""

from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
