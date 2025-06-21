from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Seance, Etudiant, Module

@login_required
def emploi_du_temps(request):
    try:
        etudiant = Etudiant.objects.get(user=request.user)
    except Etudiant.DoesNotExist:
        return render(request, 'gestion/error.html', {'message': 'Profil étudiant non trouvé'})
    
    # Récupérer la semaine actuelle
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Lundi
    end_of_week = start_of_week + timedelta(days=6)          # Dimanche
    
    # Récupérer les séances de l'étudiant
    seances = Seance.objects.filter(
        module__in=Module.objects.filter(
            inscriptionmodule__etudiant=etudiant
        )
    ).order_by('jour', 'heure_debut')
    
    # Organiser les séances par jour et créneau horaire
    emploi = {
        1: {'8h-10h': None, '10h-12h': None, '14h-16h': None, '16h-18h': None},  # Lundi
        2: {'8h-10h': None, '10h-12h': None, '14h-16h': None, '16h-18h': None},  # Mardi
        3: {'8h-10h': None, '10h-12h': None, '14h-16h': None, '16h-18h': None},  # Mercredi
        4: {'8h-10h': None, '10h-12h': None, '14h-16h': None, '16h-18h': None},  # Jeudi
        5: {'8h-10h': None, '10h-12h': None, '14h-16h': None, '16h-18h': None},  # Vendredi
        6: {'8h-10h': None, '10h-12h': None, '14h-16h': None, '16h-18h': None},  # Samedi
    }
    
    # Couleurs pour les différents modules
    module_colors = {}
    colors = ['info', 'success', 'warning', 'danger', 'primary', 'secondary']
    for i, module in enumerate(Module.objects.filter(inscriptionmodule__etudiant=etudiant)):
        module_colors[module.id] = colors[i % len(colors)]
    
    for seance in seances:
        # Déterminer le créneau horaire
        heure_debut = seance.heure_debut.hour
        if 8 <= heure_debut < 10:
            creneau = '8h-10h'
        elif 10 <= heure_debut < 12:
            creneau = '10h-12h'
        elif 14 <= heure_debut < 16:
            creneau = '14h-16h'
        elif 16 <= heure_debut < 18:
            creneau = '16h-18h'
        else:
            continue  # Autres créneaux non affichés
        
        # Vérifier si c'est un TD/TP et si l'étudiant est dans le bon groupe
        if seance.type_seance in ['TD', 'TP'] and seance.groupe and etudiant.groupe_tp != seance.groupe:
            continue
        
        emploi[seance.jour][creneau] = {
            'seance': seance,
            'color': module_colors.get(seance.module.id, 'primary')
        }
    
    context = {
        'emploi': emploi,
        'current_week': {
            'start': start_of_week,
            'end': end_of_week,
        },
        'module_colors': module_colors,
    }
    
    return render(request, 'gestion/emploi_du_temps.html', context)