"""
Formulaires pour l'application jobs.

Ce module contient les formulaires pour la création et la modification
des offres d'emploi par les entreprises.
"""

from django import forms
from .models import Offer


class OfferForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier une offre d'emploi.

    Le champ 'skills' est géré comme une liste de compétences
    séparées par des virgules pour faciliter la saisie utilisateur.
    """

    # Champ personnalisé pour les compétences (transformer JSON en chaîne)
    skills_input = forms.CharField(
        label="Compétences requises",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Énumérez les compétences séparées par des virgules (ex: Python, Django, PostgreSQL)',
            'rows': 4,
        }),
        help_text="Entrez les compétences séparées par des virgules"
    )

    class Meta:
        model = Offer
        fields = ['title', 'description', 'salary', 'active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Titre du poste (ex: Développeur Python Senior)',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Décrivez le poste, les responsabilités, l\'équipe, etc.',
                'rows': 8,
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': '35000.00',
                'step': '0.01',
            }),
            'active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 accent-primary',
            }),
        }
        labels = {
            'title': 'Titre du poste',
            'description': 'Description',
            'salary': 'Salaire (€)',
            'active': 'Offre active',
        }

    def clean_skills_input(self):
        """
        Transformer la chaîne des compétences en liste JSON.
        """
        skills_input = self.cleaned_data.get('skills_input', '')
        if skills_input.strip():
            # Séparer par virgule et nettoyer chaque compétence
            skills = [skill.strip() for skill in skills_input.split(',') if skill.strip()]
            return skills
        return []

    def save(self, commit=True):
        """
        Sauvegarder l'offre avec les compétences formatées en JSON.
        """
        instance = super().save(commit=False)
        instance.skills = self.cleaned_data.get('skills_input', [])
        if commit:
            instance.save()
        return instance

