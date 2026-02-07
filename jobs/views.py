from django.shortcuts import render

from home.decorators import login_required_custom


@login_required_custom
def index(request):
    """
    Vue d'accueil qui affiche la page index.html.
    Cette page sert de point d'entrée principale de l'application job board.
    """
    return render(request, 'jobs/index.html')
