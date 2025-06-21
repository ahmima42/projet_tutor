from django.contrib import admin
from .models import Filiere, Niveau, Module, Enseignant, Etudiant, AlerteSysteme, StatistiqueConnexion

@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ['code', 'nom', 'nombre_etudiants', 'nombre_modules', 'created_at']
    search_fields = ['code', 'nom']
    list_filter = ['created_at']

@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ['nom', 'description']

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['code', 'nom', 'filiere', 'niveau', 'coefficient', 'total_heures']
    list_filter = ['filiere', 'niveau', 'created_at']
    search_fields = ['code', 'nom']

@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = ['nom_complet', 'matricule', 'grade', 'specialite', 'created_at']
    list_filter = ['grade', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'matricule']

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ['nom_complet', 'cne', 'filiere', 'niveau', 'date_inscription']
    list_filter = ['filiere', 'niveau', 'date_inscription']
    search_fields = ['user__first_name', 'user__last_name', 'cne', 'cin']

@admin.register(AlerteSysteme)
class AlerteSystemeAdmin(admin.ModelAdmin):
    list_display = ['titre', 'type_alerte', 'lu', 'created_at']
    list_filter = ['type_alerte', 'lu', 'created_at']
    search_fields = ['titre', 'message']

@admin.register(StatistiqueConnexion)
class StatistiqueConnexionAdmin(admin.ModelAdmin):
    list_display = ['date', 'connexions', 'nouveaux_comptes']
    list_filter = ['date']
