"""
Modèles pour l'application home.

On ajoute un profil simple pour distinguer postulant et entreprise.
"""

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    USER_TYPE_APPLICANT = 'postulant'
    USER_TYPE_COMPANY = 'entreprise'
    USER_TYPE_CHOICES = [
        (USER_TYPE_APPLICANT, 'Postulant'),
        (USER_TYPE_COMPANY, 'Entreprise'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    address = models.CharField(max_length=255)
    image = models.ImageField(upload_to='profiles/images/', blank=True, null=True)
    siret = models.CharField(max_length=14, blank=True)
    cv = models.FileField(upload_to='profiles/cvs/', blank=True, null=True)  # CV pour postulants uniquement

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"

