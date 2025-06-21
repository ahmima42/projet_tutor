from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Module, Seance, InscriptionModule

@login_required
def mes_modules(request):
    # Récupérer les modules enseignés par le professeur connecté
    modules = Module.objects.filter(professeur=request.user)
    
    # Récupérer les prochaines séances pour ces modules
    prochaines_seances = Seance.objects.filter(
        module__in=modules
    ).order_by('date', 'heure_debut')[:3]
    
    # Calculer le nombre total d'étudiants dans les modules
    total_etudiants = InscriptionModule.objects.filter(
        module__in=modules
    ).values('etudiant').distinct().count()
    
    context = {
        'modules': modules,
        'nombre_modules': modules.count(),
        'total_etudiants': total_etudiants,
        'prochaines_seances': prochaines_seances,
        # Pour l'exemple, on met 15 notes à saisir (à adapter selon votre logique)
        'notes_a_saisir': 15,
    }
    
    return render(request, 'gestion/modules.html', context)

@login_required
def details_module(request, module_id):
    module = get_object_or_404(Module, id=module_id, professeur=request.user)
    inscriptions = InscriptionModule.objects.filter(module=module)
    seances = Seance.objects.filter(module=module).order_by('-date', 'heure_debut')
    
    context = {
        'module': module,
        'etudiants': [inscription.etudiant for inscription in inscriptions],
        'seances': seances,
    }
    
    return render(request, 'gestion/details_module.html', context)