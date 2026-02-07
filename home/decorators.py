"""
Décorateurs personnalisés pour l'authentification et les permissions.

Ce module fournit des décorateurs réutilisables pour protéger les vues
et contrôler l'accès en fonction du statut d'authentification.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse


def login_required_custom(view_func):
    """
    Décorateur pour protéger une vue et demander la connexion.

    Redirige les utilisateurs non authentifiés vers la page de connexion.

    Usage:
        @login_required_custom
        def my_view(request):
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Vous devez être connecté pour accéder à cette page.')
            return redirect(f"{reverse('home:login')}?next={request.path}")
        return view_func(request, *args, **kwargs)
    return wrapper


def logout_required(view_func):
    """
    Décorateur pour protéger une vue et interdire aux utilisateurs connectés.

    Redirige les utilisateurs authentifiés vers le board.

    Usage:
        @logout_required
        def my_view(request):
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'Vous êtes déjà connecté.')
            return redirect('jobs:index')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """
    Décorateur pour protéger une vue et demander les droits administrateur.

    Redirige les utilisateurs non administrateurs vers la page d'accueil.

    Usage:
        @admin_required
        def my_view(request):
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            messages.error(request, 'Vous n\'avez pas les permissions nécessaires.')
            return redirect('home:index')
        return view_func(request, *args, **kwargs)
    return wrapper

