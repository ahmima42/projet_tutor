from django.contrib import admin
from .models import Filiere, Niveau

@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ['code', 'nom', 'responsable', 'statut', 'nb_etudiants', 'created_at']
    list_filter = ['statut', 'duree_annees', 'created_at']
    search_fields = ['nom', 'code', 'responsable']

@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ['code', 'nom', 'ordre', 'nb_etudiants', 'created_at']
    list_filter = ['ordre', 'created_at']
    search_fields = ['nom', 'code']
