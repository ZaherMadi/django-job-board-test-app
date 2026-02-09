"""Administration pour l'application home."""

from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'siret')
    search_fields = ('user__username', 'user__email', 'siret')

