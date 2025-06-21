from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Filiere(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return f"{self.nom} ({self.code})"

class Niveau(models.Model):
    nom = models.CharField(max_length=50)  # Ex: "1ère année", "2ème année"
    code = models.CharField(max_length=10)  # Ex: "S1", "S2"
    
    def __str__(self):
        return f"{self.nom} ({self.code})"

class Module(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    professeur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'groups__name': 'Enseignants'})
    
    def __str__(self):
        return f"{self.nom} ({self.code})"

class Salle(models.Model):
    nom = models.CharField(max_length=50)
    capacite = models.PositiveIntegerField()
    batiment = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.nom} (Bât. {self.batiment})"

class Seance(models.Model):
    TYPE_SEANCE = [
        ('C', 'Cours'),
        ('TD', 'Travaux Dirigés'),
        ('TP', 'Travaux Pratiques'),
    ]
    
    JOURS_SEMAINE = [
        (1, 'Lundi'),
        (2, 'Mardi'),
        (3, 'Mercredi'),
        (4, 'Jeudi'),
        (5, 'Vendredi'),
        (6, 'Samedi'),
    ]
    
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    type_seance = models.CharField(max_length=2, choices=TYPE_SEANCE)
    jour = models.PositiveSmallIntegerField(choices=JOURS_SEMAINE)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    salle = models.ForeignKey(Salle, on_delete=models.SET_NULL, null=True)
    professeur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='seances_enseignees')
    groupe = models.CharField(max_length=50, blank=True, null=True)  # Pour les TD/TP par groupe
    
    class Meta:
        ordering = ['jour', 'heure_debut']
        verbose_name = "Séance"
        verbose_name_plural = "Séances"
    
    def __str__(self):
        return f"{self.module} - {self.get_type_seance_display()} {self.get_jour_display()} {self.heure_debut}-{self.heure_fin}"

class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricule = models.CharField(max_length=20, unique=True)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    groupe_tp = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.matricule})"

class InscriptionModule(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    annee_univ = models.CharField(max_length=9)  # Ex: "2023-2024"
    
    class Meta:
        unique_together = ('etudiant', 'module', 'annee_univ')
    
    def __str__(self):
        return f"{self.etudiant} inscrit à {self.module} ({self.annee_univ})"