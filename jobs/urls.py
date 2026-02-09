"""
Configuration des URLs pour l'application jobs.

Ce module définit les routes pour l'affichage des offres d'emploi.
"""

from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.index, name='index'),
]
