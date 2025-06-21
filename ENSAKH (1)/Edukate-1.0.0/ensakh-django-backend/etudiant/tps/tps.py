# backend.py
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.serializers.json import DjangoJSONEncoder
import json
from datetime import datetime

# Modèles
class Etudiant(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    avatar_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.nom

class Module(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nom

class Projet(models.Model):
    STATUS_CHOICES = [
        ('non_commence', 'Non commencé'),
        ('en_cours', 'En cours'),
        ('rendu', 'Rendu'),
    ]
    
    id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date_remise = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='non_commence')
    note = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    feedback = models.TextField(blank=True, null=True)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.titre} ({self.module})"
    
    def clean(self):
        if self.note is not None and (self.note < 0 or self.note > 20):
            raise ValidationError({'note': 'La note doit être entre 0 et 20'})

class FichierProjet(models.Model):
    projet = models.ForeignKey(Projet, related_name='fichiers', on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=20)
    taille = models.CharField(max_length=20)
    url = models.URLField()
    
    def __str__(self):
        return self.nom

class TP(models.Model):
    STATUS_CHOICES = [
        ('a_faire', 'À faire'),
        ('termine', 'Terminé'),
    ]
    
    id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    date = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='a_faire')
    note = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.titre} ({self.module})"

# Sérialiseurs
class EtudiantSerializer:
    @staticmethod
    def serialize(etudiant):
        return {
            'id': etudiant.id,
            'name': etudiant.nom,
            'email': etudiant.email,
            'avatar': etudiant.avatar_url or f"https://ui-avatars.com/api/?name={etudiant.nom.replace(' ', '+')}&background=3b82f6&color=fff"
        }

class ModuleSerializer:
    @staticmethod
    def serialize(module):
        return {
            'code': module.code,
            'nom': module.nom,
            'description': module.description
        }

class FichierProjetSerializer:
    @staticmethod
    def serialize(fichier):
        return {
            'name': fichier.nom,
            'type': fichier.type,
            'size': fichier.taille,
            'url': fichier.url
        }

class ProjetSerializer:
    @staticmethod
    def serialize(projet):
        fichiers = [FichierProjetSerializer.serialize(f) for f in projet.fichiers.all()]
        
        return {
            'id': projet.id,
            'module': projet.module.nom,
            'title': projet.titre,
            'dueDate': projet.date_remise.isoformat(),
            'status': projet.get_statut_display().lower().replace(' ', '_'),
            'grade': projet.note,
            'description': projet.description,
            'files': fichiers,
            'feedback': projet.feedback
        }

class TPSerializer:
    @staticmethod
    def serialize(tp):
        return {
            'id': tp.id,
            'module': tp.module.nom,
            'title': tp.titre,
            'date': tp.date.isoformat(),
            'status': tp.get_statut_display().lower().replace(' ', '_'),
            'grade': tp.note
        }

# Vues
@method_decorator(csrf_exempt, name='dispatch')
class APIStatusView(View):
    def get(self, request):
        return JsonResponse({'status': 'connected', 'message': 'API ENSAKH en ligne'})

@method_decorator(csrf_exempt, name='dispatch')
class EtudiantInfoView(View):
    def get(self, request, student_id):
        try:
            etudiant = Etudiant.objects.get(id=student_id)
            return JsonResponse(EtudiantSerializer.serialize(etudiant))
        except Etudiant.DoesNotExist:
            return JsonResponse({'error': 'Étudiant non trouvé'}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class ProjetStatsView(View):
    def get(self, request, student_id):
        try:
            etudiant = Etudiant.objects.get(id=student_id)
            projets = Projet.objects.filter(etudiant=etudiant)
            
            total_projets = projets.count()
            completed_projets = projets.filter(statut='rendu').count()
            in_progress_projets = projets.filter(statut='en_cours').count()
            
            notes = [p.note for p in projets.filter(statut='rendu') if p.note is not None]
            moyenne = sum(notes) / len(notes) if notes else 0
            
            return JsonResponse({
                'totalProjects': total_projets,
                'completedProjects': completed_projets,
                'inProgressProjects': in_progress_projets,
                'averageGrade': round(moyenne, 1),
                'lastUpdate': datetime.now().isoformat()
            })
        except Etudiant.DoesNotExist:
            return JsonResponse({'error': 'Étudiant non trouvé'}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class ProjetListView(View):
    def get(self, request, student_id):
        try:
            etudiant = Etudiant.objects.get(id=student_id)
            projets = Projet.objects.filter(etudiant=etudiant).select_related('module').prefetch_related('fichiers')
            
            projets_data = [ProjetSerializer.serialize(p) for p in projets]
            return JsonResponse(projets_data, safe=False)
        except Etudiant.DoesNotExist:
            return JsonResponse({'error': 'Étudiant non trouvé'}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class TPListView(View):
    def get(self, request, student_id):
        try:
            etudiant = Etudiant.objects.get(id=student_id)
            tps = TP.objects.filter(etudiant=etudiant).select_related('module')
            
            tps_data = [TPSerializer.serialize(tp) for tp in tps]
            return JsonResponse(tps_data, safe=False)
        except Etudiant.DoesNotExist:
            return JsonResponse({'error': 'Étudiant non trouvé'}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateProjetStatusView(View):
    def post(self, request, student_id, project_id):
        try:
            data = json.loads(request.body)
            nouveau_statut = data.get('status')
            
            if nouveau_statut not in [choice[0] for choice in Projet.STATUS_CHOICES]:
                return JsonResponse({'error': 'Statut invalide'}, status=400)
            
            projet = Projet.objects.get(id=project_id, etudiant_id=student_id)
            projet.statut = nouveau_statut
            projet.save()
            
            return JsonResponse({'success': True, 'new_status': projet.get_statut_display()})
        except Projet.DoesNotExist:
            return JsonResponse({'error': 'Projet non trouvé'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Données JSON invalides'}, status=400)

# Configuration des URLs
def configure_urls():
    from django.urls import path
    
    urlpatterns = [
        path('api/status/', APIStatusView.as_view(), name='api-status'),
        path('api/students/<int:student_id>/', EtudiantInfoView.as_view(), name='student-info'),
        path('api/students/<int:student_id>/projects/stats/', ProjetStatsView.as_view(), name='project-stats'),
        path('api/students/<int:student_id>/projects/', ProjetListView.as_view(), name='project-list'),
        path('api/students/<int:student_id>/tps/', TPListView.as_view(), name='tp-list'),
        path('api/students/<int:student_id>/projects/<int:project_id>/status/', UpdateProjetStatusView.as_view(), name='update-project-status'),
    ]
    
    return urlpatterns

# Initialisation des données de test
def initialize_test_data():
    # Créer un étudiant de test
    etudiant, created = Etudiant.objects.get_or_create(
        id=12345,
        defaults={
            'nom': 'Ahmed Berrada',
            'email': 'ahmed.berrada@ensakh.ma',
            'avatar_url': 'https://ui-avatars.com/api/?name=Ahmed+Berrada&background=3b82f6&color=fff'
        }
    )
    
    # Créer des modules de test
    modules = [
        Module.objects.get_or_create(
            code='WEB',
            defaults={
                'nom': 'Programmation Web',
                'description': 'Développement d\'applications web modernes'
            }
        ),
        Module.objects.get_or_create(
            code='BDD',
            defaults={
                'nom': 'Base de données',
                'description': 'Conception et implémentation de bases de données'
            }
        ),
        Module.objects.get_or_create(
            code='ALGO',
            defaults={
                'nom': 'Algorithmique',
                'description': 'Structures de données et algorithmes fondamentaux'
            }
        ),
        Module.objects.get_or_create(
            code='RES',
            defaults={
                'nom': 'Réseaux',
                'description': 'Principes des réseaux informatiques'
            }
        ),
        Module.objects.get_or_create(
            code='SYSEXP',
            defaults={
                'nom': 'Systèmes d\'exploitation',
                'description': 'Fonctionnement des systèmes d\'exploitation'
            }
        )
    ]
    
    web_module = Module.objects.get(code='WEB')
    bdd_module = Module.objects.get(code='BDD')
    algo_module = Module.objects.get(code='ALGO')
    res_module = Module.objects.get(code='RES')
    sys_module = Module.objects.get(code='SYSEXP')
    
    # Créer des projets de test
    projets = [
        Projet.objects.get_or_create(
            id=1,
            defaults={
                'module': web_module,
                'titre': 'Site e-commerce',
                'description': 'Développement d\'un site e-commerce complet avec panier, système de paiement et backoffice administrateur.',
                'date_remise': '2023-06-10',
                'statut': 'rendu',
                'note': 18.0,
                'feedback': 'Excellent travail! L\'interface est très intuitive et le code est bien structuré. Quelques améliorations possibles dans la gestion des erreurs.',
                'etudiant': etudiant
            }
        ),
        Projet.objects.get_or_create(
            id=2,
            defaults={
                'module': bdd_module,
                'titre': 'Modélisation UML',
                'description': 'Modélisation UML complète d\'un système de gestion de bibliothèque avec diagrammes de cas d\'utilisation, de classes et de séquence.',
                'date_remise': '2023-06-15',
                'statut': 'rendu',
                'note': 16.5,
                'feedback': 'Bon travail global. Les diagrammes sont clairs mais il manque quelques relations dans le diagramme de classes.',
                'etudiant': etudiant
            }
        ),
        Projet.objects.get_or_create(
            id=3,
            defaults={
                'module': algo_module,
                'titre': 'Arbres binaires',
                'description': 'Implémentation et analyse de structures d\'arbres binaires avec opérations de recherche, insertion et suppression.',
                'date_remise': '2023-06-25',
                'statut': 'en_cours',
                'note': None,
                'feedback': None,
                'etudiant': etudiant
            }
        ),
        Projet.objects.get_or_create(
            id=4,
            defaults={
                'module': res_module,
                'titre': 'Simulation TCP/IP',
                'description': 'Simulation du protocole TCP/IP avec analyse des performances et gestion des erreurs.',
                'date_remise': '2023-06-30',
                'statut': 'non_commence',
                'note': None,
                'feedback': None,
                'etudiant': etudiant
            }
        )
    ]
    
    # Ajouter des fichiers aux projets
    projet1 = Projet.objects.get(id=1)
    FichierProjet.objects.get_or_create(
        projet=projet1,
        nom='rapport.pdf',
        type='pdf',
        taille='2.4 MB',
        url='/files/rapport.pdf'
    )
    FichierProjet.objects.get_or_create(
        projet=projet1,
        nom='code-source.zip',
        type='zip',
        taille='5.1 MB',
        url='/files/code-source.zip'
    )
    FichierProjet.objects.get_or_create(
        projet=projet1,
        nom='presentation.pptx',
        type='ppt',
        taille='3.7 MB',
        url='/files/presentation.pptx'
    )
    
    projet2 = Projet.objects.get(id=2)
    FichierProjet.objects.get_or_create(
        projet=projet2,
        nom='modele.asta',
        type='file',
        taille='1.2 MB',
        url='/files/modele.asta'
    )
    FichierProjet.objects.get_or_create(
        projet=projet2,
        nom='rapport.docx',
        type='word',
        taille='1.8 MB',
        url='/files/rapport.docx'
    )
    
    # Créer des TPs de test
    TP.objects.get_or_create(
        id=1,
        defaults={
            'module': sys_module,
            'titre': 'TP4 - Gestion processus',
            'date': '2023-06-05',
            'statut': 'termine',
            'note': 14.0,
            'etudiant': etudiant
        }
    )
    TP.objects.get_or_create(
        id=2,
        defaults={
            'module': web_module,
            'titre': 'TP3 - JavaScript',
            'date': '2023-06-12',
            'statut': 'termine',
            'note': 17.5,
            'etudiant': etudiant
        }
    )
    TP.objects.get_or_create(
        id=3,
        defaults={
            'module': bdd_module,
            'titre': 'TP5 - Requêtes SQL',
            'date': '2023-06-20',
            'statut': 'a_faire',
            'note': None,
            'etudiant': etudiant
        }
    )

# Point d'entrée pour Django
def get_urls():
    # Cette fonction est utilisée par Django pour configurer les URLs
    return configure_urls()

# Pour initialiser les données de test lors du premier lancement
if __name__ == '__main__':
    import os
    import django
    from django.conf import settings
    
    # Configuration minimale de Django
    if not settings.configured:
        settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': 'ensakh.db',
                }
            },
            INSTALLED_APPS=[
                'django.contrib.contenttypes',
                'django.contrib.auth',
            ],
            DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
        )
        django.setup()
    
    # Créer les tables si elles n'existent pas
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        if not tables:
            print("Création des tables...")
            from django.core.management.commands import migrate
            migrate.Command().handle()
            
            # Initialiser les données de test
            print("Initialisation des données de test...")
            initialize_test_data()
            print("Données initialisées avec succès!")
    
    # Démarrer le serveur de développement
    from django.core.management.commands import runserver
    print("Serveur backend Django démarré sur http://localhost:8000")
    runserver.Command().handle()