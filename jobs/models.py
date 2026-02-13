"""
Modèles pour l'application jobs (offres d'emploi).

Ce module contient le modèle Offer qui représente une offre d'emploi
publiée par une entreprise.
"""

from django.db import models
from django.contrib.auth.models import User
from home.models import Profile


class Offer(models.Model):
    """
    Modèle représentant une offre d'emploi.

    Attributs:
        - id: Clé primaire (généré automatiquement)
        - company: FK vers le profil entreprise (User avec Profile user_type='entreprise')
        - title: Titre de l'offre
        - description: Description détaillée de l'offre
        - salary: Salaire proposé (optionnel)
        - skills: Liste de compétences requises au format JSON
        - publication_date: Date/heure de publication (auto-générée)
        - active: Statut de l'offre (active ou archivée)
    """
    company = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='offers',
        help_text="Entreprise qui publie l'offre"
    )
    title = models.CharField(
        max_length=255,
        help_text="Titre de l'offre d'emploi"
    )
    description = models.TextField(
        help_text="Description détaillée du poste et des responsabilités"
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Salaire proposé (optionnel)"
    )
    skills = models.JSONField(
        default=list,
        blank=True,
        help_text="Liste de compétences requises"
    )
    publication_date = models.DateTimeField(
        auto_now_add=True,
        help_text="Date et heure de publication automatiques"
    )
    active = models.BooleanField(
        default=True,
        help_text="L'offre est-elle active?"
    )

    class Meta:
        verbose_name = "Offre d'emploi"
        verbose_name_plural = "Offres d'emploi"
        ordering = ['-publication_date']

    def __str__(self):
        return f"{self.title} - {self.company.profile.user} ({self.publication_date.year})"
