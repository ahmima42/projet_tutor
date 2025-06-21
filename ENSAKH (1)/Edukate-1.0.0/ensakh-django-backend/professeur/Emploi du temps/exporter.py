from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from ics import Calendar, Event
from datetime import datetime

@login_required
def export_emploi_pdf(request):
    try:
        etudiant = Etudiant.objects.get(user=request.user)
    except Etudiant.DoesNotExist:
        return HttpResponse("Profil étudiant non trouvé", status=404)
    
    # Récupérer les données comme dans la vue emploi_du_temps
    seances = Seance.objects.filter(
        module__in=Module.objects.filter(
            inscriptionmodule__etudiant=etudiant
        )
    ).order_by('jour', 'heure_debut')
    
    # Générer le HTML
    html_string = render_to_string('gestion/export_emploi_pdf.html', {
        'seances': seances,
        'etudiant': etudiant,
        'date_export': timezone.now().date()
    })
    
    # Créer le PDF
    html = HTML(string=html_string)
    result = html.write_pdf()
    
    # Créer la réponse
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="emploi_du_temps_{etudiant.matricule}.pdf"'
    response.write(result)
    
    return response

@login_required
def export_emploi_ical(request):
    try:
        etudiant = Etudiant.objects.get(user=request.user)
    except Etudiant.DoesNotExist:
        return HttpResponse("Profil étudiant non trouvé", status=404)
    
    # Créer un nouveau calendrier
    cal = Calendar()
    
    # Ajouter les événements pour chaque séance
    seances = Seance.objects.filter(
        module__in=Module.objects.filter(
            inscriptionmodule__etudiant=etudiant
        )
    )
    
    for seance in seances:
        event = Event()
        event.name = f"{seance.module.nom} ({seance.get_type_seance_display()})"
        event.description = f"Professeur: {seance.professeur.get_full_name()}\nSalle: {seance.salle.nom}"
        event.location = f"Bât. {seance.salle.batiment}, {seance.salle.nom}"
        
        # Déterminer la date (on prend la semaine courante)
        today = timezone.now().date()
        days_until_seance_day = seance.jour - today.weekday() - 1
        seance_date = today + timedelta(days=days_until_seance_day)
        
        # Combiner avec l'heure
        event.begin = datetime.combine(seance_date, seance.heure_debut)
        event.end = datetime.combine(seance_date, seance.heure_fin)
        
        cal.events.add(event)
    
    # Retourner le fichier iCal
    response = HttpResponse(cal.serialize(), content_type='text/calendar')
    response['Content-Disposition'] = f'attachment; filename="emploi_du_temps_{etudiant.matricule}.ics"'
    return response