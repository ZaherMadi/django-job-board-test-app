from django.shortcuts import render

def index(request):
    """
    Vue d'accueil qui affiche la page index.html.
    Cette page sert de point d'entrée principal de l'application job board.
    """
    return render(request, 'index.html')
