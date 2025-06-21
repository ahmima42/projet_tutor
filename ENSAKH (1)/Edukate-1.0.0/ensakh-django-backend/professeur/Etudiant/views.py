from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Etudiant, Module, Note, Filiere, Niveau
from .serializers import EtudiantSerializer, NoteSerializer
import json

@login_required
def dashboard_professeur(request):
    return render(request, 'professeur.html')

@login_required
def liste_etudiants(request):
    # Récupérer les paramètres de filtrage
    module_id = request.GET.get('module')
    niveau_id = request.GET.get('niveau')
    search_query = request.GET.get('search', '')
    
    # Filtrer les étudiants
    etudiants = Etudiant.objects.all()
    
    if search_query:
        etudiants = etudiants.filter(
            models.Q(user__first_name__icontains=search_query) |
            models.Q(user__last_name__icontains=search_query) |
            models.Q(cne__icontains=search_query)
        )
    
    if module_id:
        module = get_object_or_404(Module, id=module_id)
        notes = Note.objects.filter(module=module)
        etudiants = etudiants.filter(id__in=[note.etudiant.id for note in notes])
    
    if niveau_id:
        niveau = get_object_or_404(Niveau, id=niveau_id)
        etudiants = etudiants.filter(niveau=niveau)
    
    # Pagination
    paginator = Paginator(etudiants, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Récupérer tous les modules et niveaux pour les filtres
    modules = Module.objects.filter(professeur=request.user)
    niveaux = Niveau.objects.filter(module__professeur=request.user).distinct()
    
    context = {
        'etudiants': page_obj,
        'modules': modules,
        'niveaux': niveaux,
        'total_etudiants': etudiants.count(),
    }
    
    return render(request, 'etudiant.html', context)

@login_required
def details_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    notes = Note.objects.filter(etudiant=etudiant)
    
    if request.method == 'POST':
        # Mettre à jour les notes
        for note in notes:
            note_key = f"note_{note.id}"
            if note_key in request.POST:
                note.valeur = request.POST[note_key]
                note.save()
    
    context = {
        'etudiant': etudiant,
        'notes': notes,
    }
    
    return render(request, 'partials/etudiant_details.html', context)

@login_required
def api_etudiants(request):
    etudiants = Etudiant.objects.all()
    serializer = EtudiantSerializer(etudiants, many=True)
    return JsonResponse(serializer.data, safe=False)

@login_required
def api_notes_etudiant(request, etudiant_id):
    notes = Note.objects.filter(etudiant_id=etudiant_id)
    serializer = NoteSerializer(notes, many=True)
    return JsonResponse(serializer.data, safe=False)