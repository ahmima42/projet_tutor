from django.db import models
from django.contrib.auth.models import User

class Filiere(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom

class Niveau(models.Model):
    nom = models.CharField(max_length=50)  # Ex: "1ère année", "2ème année"
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} - {self.filiere.nom}"

class Module(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    professeur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nom} ({self.code})"

class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cne = models.CharField(max_length=20, unique=True)
    date_naissance = models.DateField(null=True, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='etudiants/', null=True, blank=True)
    niveau = models.ForeignKey(Niveau, on_delete=models.SET_NULL, null=True)
    date_inscription = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.cne})"

class Note(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    valeur = models.DecimalField(max_digits=4, decimal_places=2)
    date_evaluation = models.DateField(auto_now_add=True)
    remarque = models.TextField(blank=True)

    class Meta:
        unique_together = ('etudiant', 'module')

    def __str__(self):
        return f"{self.etudiant} - {self.module}: {self.valeur}"