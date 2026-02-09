"""
Formulaires d'authentification pour l'application job board.

Ce module contient les formulaires utilisés pour l'enregistrement et la connexion
des utilisateurs. Ils utilisent les fonctionnalités de validation intégrées de Django.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class RegisterForm(UserCreationForm):
    """
    Formulaire d'enregistrement personnalisé basé sur UserCreationForm de Django.

    Ajoute les champs email et prénom/nom pour enrichir le profil utilisateur.
    """
    user_type = forms.ChoiceField(
        choices=Profile.USER_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary',
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'your@email.com'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
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
    address = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Adresse'
        })
    )
    image = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'URL de l\'image (optionnel)'
        })
    )
    siret = forms.CharField(
        max_length=14,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'SIRET (pour entreprise)'
        })
    )

    class Meta:
        model = User
        fields = ('user_type', 'first_name', 'last_name', 'username', 'email', 'address', 'image', 'siret', 'password1', 'password2')
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

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        first_name = (cleaned_data.get('first_name') or '').strip()
        siret = (cleaned_data.get('siret') or '').strip()

        if user_type == Profile.USER_TYPE_APPLICANT and not first_name:
            self.add_error('first_name', 'Le prénom est requis pour un postulant.')

        if user_type == Profile.USER_TYPE_COMPANY:
            if not siret:
                self.add_error('siret', 'Le SIRET est requis pour une entreprise.')
            elif not (siret.isdigit() and len(siret) == 14):
                self.add_error('siret', 'Le SIRET doit contenir exactement 14 chiffres.')

        return cleaned_data

    def save(self, commit=True):
        """Sauvegarder l'utilisateur avec l'email et le profil dans la base de données."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                user_type=self.cleaned_data['user_type'],
                address=self.cleaned_data['address'],
                image=self.cleaned_data.get('image', ''),
                siret=self.cleaned_data.get('siret', ''),
            )
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


class ProfileUpdateForm(forms.Form):
    """Formulaire simple pour mettre à jour le profil utilisateur."""
    _input_classes = 'w-full px-4 py-3 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all'

    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': _input_classes})
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': _input_classes})
    )
    address = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': _input_classes})
    )
    image = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': _input_classes})
    )
    siret = forms.CharField(
        max_length=14,
        required=False,
        widget=forms.TextInput(attrs={'class': _input_classes})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.profile = kwargs.pop('profile')
        super().__init__(*args, **kwargs)
        if not self.is_bound:
            self.initial.update({
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'address': self.profile.address,
                'image': self.profile.image,
                'siret': self.profile.siret,
            })

    def clean(self):
        cleaned_data = super().clean()
        first_name = (cleaned_data.get('first_name') or '').strip()
        siret = (cleaned_data.get('siret') or '').strip()

        if self.profile.user_type == Profile.USER_TYPE_APPLICANT and not first_name:
            self.add_error('first_name', 'Le prénom est requis pour un postulant.')

        if self.profile.user_type == Profile.USER_TYPE_COMPANY:
            if not siret:
                self.add_error('siret', 'Le SIRET est requis pour une entreprise.')
            elif not (siret.isdigit() and len(siret) == 14):
                self.add_error('siret', 'Le SIRET doit contenir exactement 14 chiffres.')

        return cleaned_data

    def save(self):
        self.user.first_name = (self.cleaned_data.get('first_name') or '').strip()
        self.user.last_name = self.cleaned_data['last_name']
        self.user.save()

        self.profile.address = self.cleaned_data['address']
        self.profile.image = self.cleaned_data.get('image', '')
        self.profile.siret = self.cleaned_data.get('siret', '')
        self.profile.save()
        return self.profile

