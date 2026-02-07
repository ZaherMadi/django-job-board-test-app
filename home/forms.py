"""
Formulaires d'authentification pour l'application job board.

Ce module contient les formulaires utilisés pour l'enregistrement et la connexion
des utilisateurs. Ils utilisent les fonctionnalités de validation intégrées de Django.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    """
    Formulaire d'enregistrement personnalisé basé sur UserCreationForm de Django.

    Ajoute les champs email et prénom/nom pour enrichir le profil utilisateur.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'your@email.com'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Prénom'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Nom'
        })
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Nom d\'utilisateur'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Styliser les champs de mot de passe
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Mot de passe'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Confirmer le mot de passe'
        })

    def save(self, commit=True):
        """Sauvegarder l'utilisateur avec l'email dans la base de données."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """
    Formulaire de connexion simple avec username et password.

    Ce formulaire est utilisé pour l'authentification des utilisateurs existants.
    """
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Nom d\'utilisateur'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Mot de passe'
        })
    )

