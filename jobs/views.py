"""
Vues pour l'application jobs (offres d'emploi).

Ce module contient les vues pour afficher, créer et supprimer des offres d'emploi.
Les entreprises peuvent publier et gérer leurs offres.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from home.decorators import login_required_custom
from .models import Offer
from .forms import OfferForm


@login_required_custom
def index(request):
    """
    Vue d'accueil qui affiche toutes les offres d'emploi actives.
    Cette page sert de point d'entrée principale du job board.
    """
    offers = Offer.objects.filter(active=True)
    return render(request, 'jobs/index.html', {'offers': offers})


@login_required
def create_offer(request):
    """
    Vue pour créer une nouvelle offre d'emploi.

    Réservée aux entreprises (user_type='entreprise').

    Méthode GET : Affiche le formulaire de création.
    Méthode POST : Traite les données et crée l'offre.

    Redirection:
        - Si l'utilisateur n'est pas une entreprise, redirection vers le board.
        - Après création, redirection vers le board.
    """
    # Vérifier que l'utilisateur est une entreprise
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'entreprise':
        messages.error(request, "Seules les entreprises peuvent publier des offres d'emploi.")
        return redirect('jobs:index')

    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            # Créer l'offre avec le user courant (entreprise)
            offer = form.save(commit=False)
            offer.company = request.user
            offer.save()

            messages.success(request, f"Offre '{offer.title}' publiée avec succès!")
            return redirect('jobs:index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = OfferForm()

    return render(request, 'jobs/create_offer.html', {'form': form})


@login_required
def delete_offer(request, offer_id):
    """
    Vue pour supprimer une offre d'emploi.

    Réservée aux entreprises propriétaires de l'offre.

    Méthode POST : Supprime l'offre

    Sécurité:
        - Vérifie que l'utilisateur est connecté
        - Vérifie que l'utilisateur est propriétaire de l'offre
        - Redirection avec message de confirmation
    """
    # Récupérer l'offre
    offer = get_object_or_404(Offer, id=offer_id)

    # Vérifier que l'utilisateur est le propriétaire
    if offer.company != request.user:
        messages.error(request, "Vous n'avez pas la permission de supprimer cette offre.")
        return redirect('jobs:index')

    # Supprimer l'offre
    offer_title = offer.title
    offer.delete()

    messages.success(request, f"Offre '{offer_title}' supprimée avec succès!")
    return redirect('jobs:index')


