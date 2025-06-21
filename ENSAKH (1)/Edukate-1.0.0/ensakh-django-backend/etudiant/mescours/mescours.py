from django.shortcuts import render
from django.db import models

# MODELES

class Etudiant(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Module(models.Model):
    nom = models.CharField(max_length=100)
    professeur = models.CharField(max_length=100)
    horaires = models.CharField(max_length=100)
    salle = models.CharField(max_length=50)
    progression = models.IntegerField()
    note = models.FloatField()
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='modules')

    def __str__(self):
        return self.nom

class Ressource(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='ressources')
    titre = models.CharField(max_length=200)
    type = models.CharField(max_length=10)  # PDF, ZIP, DOCX
    taille = models.CharField(max_length=20)
    date = models.DateField()

    def __str__(self):
        return self.titre


# VUE

from django.utils.html import format_html

def mes_cours(request):
    etudiant = Etudiant.objects.first()  # par défaut, prendre le premier étudiant
    modules = etudiant.modules.all()

    ressources = Ressource.objects.all()

    context = {
        'etudiant': etudiant,
        'modules': modules,
        'ressources': ressources,
    }

    return render(request, 'mes_cours.html', context)
