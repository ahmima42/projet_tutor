from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Filiere, Module, Enseignant, Etudiant, AlerteSysteme, StatistiqueConnexion
import json

def login_view(request):
    """Vue de connexion"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    
    return render(request, 'registration/login.html')

def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    """Vue principale du tableau de bord"""
    # Statistiques générales
    stats = {
        'total_etudiants': Etudiant.objects.count(),
        'total_enseignants': Enseignant.objects.count(),
        'total_modules': Module.objects.count(),
        'total_filieres': Filiere.objects.count(),
    }
    
    # Répartition par filière
    filieres_stats = Filiere.objects.annotate(
        nb_etudiants=Count('etudiants')
    ).values('code', 'nom', 'nb_etudiants')
    
    # Derniers utilisateurs ajoutés
    derniers_etudiants = Etudiant.objects.select_related('user', 'filiere').order_by('-created_at')[:5]
    derniers_enseignants = Enseignant.objects.select_related('user').order_by('-created_at')[:3]
    
    # Alertes système
    alertes = AlerteSysteme.objects.filter(lu=False).order_by('-created_at')[:5]
    
    # Statistiques de connexion (6 derniers mois)
    six_mois_ago = timezone.now().date() - timedelta(days=180)
    stats_connexion = StatistiqueConnexion.objects.filter(
        date__gte=six_mois_ago
    ).order_by('date')
    
    # Préparer les données pour les graphiques
    chart_data = {
        'labels': [stat.date.strftime('%b') for stat in stats_connexion],
        'connexions': [stat.connexions for stat in stats_connexion],
        'nouveaux_comptes': [stat.nouveaux_comptes for stat in stats_connexion],
    }
    
    context = {
        'stats': stats,
        'filieres_stats': list(filieres_stats),
        'derniers_etudiants': derniers_etudiants,
        'derniers_enseignants': derniers_enseignants,
        'alertes': alertes,
        'chart_data': json.dumps(chart_data),
    }
    
    return render(request, 'dashboard/index.html', context)

@login_required
def gestion_modules_view(request):
    """Vue de gestion des modules"""
    modules = Module.objects.select_related('filiere', 'niveau').order_by('filiere', 'niveau', 'code')
    filieres = Filiere.objects.all()
    
    context = {
        'modules': modules,
        'filieres': filieres,
    }
    
    return render(request, 'dashboard/gestion_modules.html', context)

@login_required
def filieres_view(request):
    """Vue de gestion des filières"""
    filieres = Filiere.objects.annotate(
        nb_etudiants=Count('etudiants'),
        nb_modules=Count('modules')
    ).order_by('code')
    
    context = {
        'filieres': filieres,
    }
    
    return render(request, 'dashboard/filieres.html', context)

@login_required
def statistiques_view(request):
    """Vue des statistiques détaillées"""
    # Statistiques par filière
    filieres_stats = Filiere.objects.annotate(
        nb_etudiants=Count('etudiants'),
        nb_modules=Count('modules')
    ).values('code', 'nom', 'nb_etudiants', 'nb_modules')
    
    # Évolution des inscriptions
    stats_mensuelles = []
    for i in range(12):
        date_debut = timezone.now().date().replace(day=1) - timedelta(days=30*i)
        date_fin = date_debut + timedelta(days=30)
        
        nb_inscriptions = Etudiant.objects.filter(
            date_inscription__gte=date_debut,
            date_inscription__lt=date_fin
        ).count()
        
        stats_mensuelles.append({
            'mois': date_debut.strftime('%b %Y'),
            'inscriptions': nb_inscriptions
        })
    
    stats_mensuelles.reverse()
    
    context = {
        'filieres_stats': list(filieres_stats),
        'stats_mensuelles': stats_mensuelles,
    }
    
    return render(request, 'dashboard/statistiques.html', context)
