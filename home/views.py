"""
Vues pour l'authentification et l'accueil de l'application job board.

Ce module contient les vues pour gérer l'enregistrement, la connexion et
la déconnexion des utilisateurs.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from .decorators import logout_required
from .models import Profile


def index(request):
    """
    Vue d'accueil qui affiche la page index.html.
    Cette page sert de point d'entrée principal de l'application job board.
    """
    return render(request, 'index.html')


@logout_required
def register(request):
    """
    Vue pour l'enregistrement d'un nouvel utilisateur.

    Méthode GET : Affiche le formulaire d'enregistrement.
    Méthode POST : Traite les données du formulaire et crée un nouvel utilisateur.

    Les utilisateurs déjà connectés sont redirigés vers le board.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Créer le nouvel utilisateur
            user = form.save()
            # Authentifier automatiquement l'utilisateur
            login(request, user)
            messages.success(request, f'Bienvenue {user.first_name}! Votre compte a été créé avec succès.')
            # Rediriger vers le board des offres d'emploi
            return redirect('jobs:index')
        else:
            # Afficher les erreurs du formulaire
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegisterForm()

    return render(request, 'home/register.html', {'form': form})


@logout_required
def login_view(request):
    """
    Vue pour la connexion d'un utilisateur existant.

    Méthode GET : Affiche le formulaire de connexion.
    Méthode POST : Authentifie l'utilisateur.

    Les utilisateurs déjà connectés sont redirigés vers le board.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Authentifier l'utilisateur
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # L'authentification a réussi
                login(request, user)
                messages.success(request, f'Bienvenue {user.first_name or user.username}!')
                # Rediriger vers le board des offres d'emploi
                return redirect('jobs:index')
            else:
                # L'authentification a échoué
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    else:
        form = LoginForm()

    return render(request, 'home/login.html', {'form': form})


@login_required(login_url='home:login')
def profile(request):
    """
    Vue du profil utilisateur.

    Affiche et met à jour les informations du compte connecté.
    """
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            'user_type': Profile.USER_TYPE_APPLICANT,
            'address': '',
        }
    )

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, user=request.user, profile=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour.')
            return redirect('home:profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProfileUpdateForm(user=request.user, profile=profile)

    return render(request, 'home/profile.html', {'form': form, 'profile': profile})


@login_required(login_url='home:login')
def logout_view(request):
    """
    Vue pour la déconnexion d'un utilisateur.

    Déconnecte l'utilisateur et le redirige vers la page d'accueil.
    """
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('home:index')
