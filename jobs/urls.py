"""
Configuration des URLs pour l'application jobs.

Ce module définit les routes pour l'affichage et la gestion des offres d'emploi.
"""

from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_offer, name='create_offer'),
    path('<int:offer_id>/delete/', views.delete_offer, name='delete_offer'),
]
