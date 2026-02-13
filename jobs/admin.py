"""
Configuration de l'admin Django pour l'application jobs.

Permet aux administrateurs de gérer les offres d'emploi.
"""

from django.contrib import admin
from .models import Offer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """
    Interface d'administration pour les offres d'emploi.

    Affiche les offres avec filtrage par entreprise, statut et date.
    """
    list_display = ('title', 'company', 'salary', 'active', 'publication_date')
    list_filter = ('active', 'publication_date', 'company')
    search_fields = ('title', 'description', 'company__user__username', 'company__user__email')
    readonly_fields = ('publication_date',)

    fieldsets = (
        ('Informations de base', {
            'fields': ('company', 'title', 'description')
        }),
        ('Détails', {
            'fields': ('salary', 'skills', 'active')
        }),
        ('Dates', {
            'fields': ('publication_date',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """
        Si l'utilisateur n'est pas superadmin, ne montrer que ses offres.
        """
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(company=request.user)
        return qs

