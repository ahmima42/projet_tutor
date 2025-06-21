from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Filiere, Niveau

def filieres_niveaux_view(request):
    """Vue principale pour la gestion des filières et niveaux"""
    filieres = Filiere.objects.filter(statut='active').order_by('code')
    niveaux = Niveau.objects.all().order_by('ordre')
    
    context = {
        'filieres': filieres,
        'niveaux': niveaux,
    }
    return render(request, 'filieres/index.html', context)

def ajouter_filiere(request):
    """Ajouter une nouvelle filière"""
    if request.method == 'POST':
        try:
            filiere = Filiere.objects.create(
                nom=request.POST.get('nom'),
                code=request.POST.get('code'),
                description=request.POST.get('description'),
                responsable=request.POST.get('responsable'),
                couleur_primaire=request.POST.get('couleur_primaire', '#667eea'),
                couleur_secondaire=request.POST.get('couleur_secondaire', '#764ba2'),
                duree_annees=int(request.POST.get('duree_annees', 3)),
                capacite_max=int(request.POST.get('capacite_max')),
                statut=request.POST.get('statut', 'active')
            )
            messages.success(request, f'Filière {filiere.nom} ajoutée avec succès!')
            return JsonResponse({'success': True, 'message': 'Filière ajoutée avec succès!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erreur: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})

def ajouter_niveau(request):
    """Ajouter un nouveau niveau"""
    if request.method == 'POST':
        try:
            niveau = Niveau.objects.create(
                nom=request.POST.get('nom'),
                code=request.POST.get('code'),
                ordre=int(request.POST.get('ordre')),
                semestre1=request.POST.get('semestre1'),
                semestre2=request.POST.get('semestre2'),
                description=request.POST.get('description', '')
            )
            messages.success(request, f'Niveau {niveau.nom} ajouté avec succès!')
            return JsonResponse({'success': True, 'message': 'Niveau ajouté avec succès!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erreur: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})

def supprimer_filiere(request, filiere_id):
    """Supprimer une filière"""
    if request.method == 'POST':
        try:
            filiere = get_object_or_404(Filiere, id=filiere_id)
            nom_filiere = filiere.nom
            filiere.delete()
            return JsonResponse({'success': True, 'message': f'Filière {nom_filiere} supprimée avec succès!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erreur: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})

def supprimer_niveau(request, niveau_id):
    """Supprimer un niveau"""
    if request.method == 'POST':
        try:
            niveau = get_object_or_404(Niveau, id=niveau_id)
            nom_niveau = niveau.nom
            niveau.delete()
            return JsonResponse({'success': True, 'message': f'Niveau {nom_niveau} supprimé avec succès!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erreur: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})
