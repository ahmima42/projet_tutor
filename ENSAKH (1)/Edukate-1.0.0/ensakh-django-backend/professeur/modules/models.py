from django.db import models
from django.contrib.auth.models import User

class Filiere(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.nom

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
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.nom} ({self.code})"

class Seance(models.Model):
    TYPE_SEANCE = [
        ('C', 'Cours'),
        ('TD', 'Travaux Dirigés'),
        ('TP', 'Travaux Pratiques'),
    ]
    
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    type_seance = models.CharField(max_length=2, choices=TYPE_SEANCE)
    date = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    salle = models.CharField(max_length=50)
    sujet = models.CharField(max_length=200)
    
    class Meta:
        ordering = ['date', 'heure_debut']
    
    def __str__(self):
        return f"{self.module} - {self.get_type_seance_display()} le {self.date}"

class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricule = models.CharField(max_length=20, unique=True)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    date_naissance = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='etudiants/', null=True, blank=True)
    
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