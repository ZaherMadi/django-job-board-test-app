 #!/usr/bin/env python3
"""
Script de test pour la fonctionnalité de publication d'offres d'emploi.

Usage:
    python test_offers.py
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_board.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from home.models import Profile
from jobs.models import Offer
from jobs.forms import OfferForm

def test_offer_model():
    """Test du modèle Offer"""
    print("🧪 Test 1: Modèle Offer")
    print("=" * 60)

    # Créer un utilisateur entreprise de test
    try:
        company_user = User.objects.get(username='test_company')
    except User.DoesNotExist:
        print("  → Création d'un utilisateur entreprise de test...")
        company_user = User.objects.create_user(
            username='test_company',
            email='company@test.com',
            password='testpass123',
            first_name='',
            last_name='Tech Corp'
        )
        profile = Profile.objects.create(
            user=company_user,
            user_type='entreprise',
            address='123 Rue de Paris',
            siret='12345678901234'
        )
        print(f"  ✓ Utilisateur créé: {company_user.username}")
        print(f"  ✓ Profil créé: {profile}")

    # Créer une offre de test
    print("\n  → Création d'une offre de test...")
    offer = Offer.objects.create(
        company=company_user,
        title="Développeur Python Senior",
        description="Rejoignez notre équipe de développeurs passionnés.",
        salary=50000,
        skills=["Python", "Django", "PostgreSQL", "Docker"],
        active=True
    )
    print(f"  ✓ Offre créée: {offer}")
    print(f"    - Titre: {offer.title}")
    print(f"    - Entreprise: {offer.company.last_name}")
    print(f"    - Compétences: {offer.skills}")
    print(f"    - Active: {offer.active}")

    # Vérifier le nombre d'offres
    count = Offer.objects.count()
    print(f"\n  ✓ Nombre total d'offres: {count}")

    return True

def test_offer_form():
    """Test du formulaire OfferForm"""
    print("\n🧪 Test 2: Formulaire OfferForm")
    print("=" * 60)

    # Récupérer ou créer l'utilisateur
    company_user = User.objects.get(username='test_company')

    # Test de création via formulaire
    print("  → Test de validation du formulaire...")

    form_data = {
        'title': 'Chef de Projet Agile',
        'description': 'Manager une équipe de 8 développeurs sur projet critique.',
        'salary': 45000,
        'active': True,
        'skills_input': 'Agile, Scrum, Leadership, Communication'
    }

    form = OfferForm(form_data)

    if form.is_valid():
        print("  ✓ Formulaire valide")
        print(f"  ✓ Compétences traitées: {form.cleaned_data['skills_input']}")

        # Sauvegarder l'offre
        offer = form.save(commit=False)
        offer.company = company_user
        offer.save()
        print(f"  ✓ Offre créée via formulaire: {offer.title}")
    else:
        print(f"  ✗ Erreurs du formulaire: {form.errors}")
        return False

    return True

def test_offer_filtering():
    """Test du filtrage des offres"""
    print("\n🧪 Test 3: Filtrage des offres")
    print("=" * 60)

    # Offres actives
    active_offers = Offer.objects.filter(active=True)
    print(f"  ✓ Offres actives: {active_offers.count()}")
    for offer in active_offers:
        print(f"    - {offer.title}")

    # Offres par entreprise
    company_user = User.objects.get(username='test_company')
    company_offers = Offer.objects.filter(company=company_user)
    print(f"\n  ✓ Offres de {company_user.last_name}: {company_offers.count()}")

    # Tri par date
    recent_offers = Offer.objects.all().order_by('-publication_date')[:2]
    print(f"\n  ✓ 2 offres les plus récentes:")
    for offer in recent_offers:
        print(f"    - {offer.title} ({offer.publication_date.strftime('%d/%m/%Y')})")

    return True

def test_admin_access():
    """Test de l'accès admin"""
    print("\n🧪 Test 4: Configuration Admin")
    print("=" * 60)

    from django.contrib import admin
    from jobs.admin import OfferAdmin
    from jobs.models import Offer

    # Vérifier l'enregistrement
    if Offer in admin.site._registry:
        print("  ✓ Modèle Offer enregistré dans l'admin")
        offer_admin = admin.site._registry[Offer]
        print(f"  ✓ Admin class: {offer_admin.__class__.__name__}")
        print(f"  ✓ List display: {offer_admin.list_display}")
        print(f"  ✓ Search fields: {offer_admin.search_fields}")
    else:
        print("  ✗ Modèle Offer NON enregistré dans l'admin")
        return False

    return True

def main():
    """Fonction principale"""
    print("\n" + "=" * 60)
    print("🚀 TESTS DE LA FONCTIONNALITÉ DE PUBLICATION D'OFFRES")
    print("=" * 60 + "\n")

    tests = [
        test_offer_model,
        test_offer_form,
        test_offer_filtering,
        test_admin_access,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n  ✗ Erreur: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)

    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"✓ Réussis: {passed}/{total}")

    if all(results):
        print("\n🎉 TOUS LES TESTS SONT PASSÉS!")
        print("\nVous pouvez maintenant:")
        print("  1. Vous enregistrer comme entreprise")
        print("  2. Aller sur /board/create/ pour publier une offre")
        print("  3. Voir l'offre sur /board/")
        print("  4. Gérer l'offre via /admin/jobs/offer/")
        return 0
    else:
        print("\n⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        return 1

if __name__ == '__main__':
    sys.exit(main())

