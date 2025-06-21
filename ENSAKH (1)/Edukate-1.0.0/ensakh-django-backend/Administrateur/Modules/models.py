from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Filiere(models.Model):
    """Modèle pour les filières"""
    code = models.CharField(max_length=10, unique=True, verbose_name="Code")
    nom = models.CharField(max_length=100, verbose_name="Nom complet")
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Filière"
        verbose_name_plural = "Filières"
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.nom}"

    @property
    def nombre_etudiants(self):
        return self.etudiants.count()

    @property
    def nombre_modules(self):
        return self.modules.count()

class Niveau(models.Model):
    """Modèle pour les niveaux d'études"""
    NIVEAUX_CHOICES = [
        ('1A', 'Première Année'),
        ('2A', 'Deuxième Année'),
        ('3A', 'Troisième Année'),
    ]
    
    nom = models.CharField(max_length=2, choices=NIVEAUX_CHOICES, unique=True)
    description = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = "Niveau"
        verbose_name_plural = "Niveaux"
        ordering = ['nom']

    def __str__(self):
        return self.get_nom_display()

class Module(models.Model):
    """Modèle pour les modules d'enseignement"""
    code = models.CharField(max_length=20, unique=True, verbose_name="Code")
    nom = models.CharField(max_length=100, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='modules')
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='modules')
    coefficient = models.IntegerField(default=1, verbose_name="Coefficient")
    heures_cours = models.IntegerField(default=0, verbose_name="Heures de cours")
    heures_td = models.IntegerField(default=0, verbose_name="Heures de TD")
    heures_tp = models.IntegerField(default=0, verbose_name="Heures de TP")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"
        ordering = ['filiere', 'niveau', 'code']

    def __str__(self):
        return f"{self.code} - {self.nom}"

    @property
    def total_heures(self):
        return self.heures_cours + self.heures_td + self.heures_tp

class Enseignant(models.Model):
    """Modèle pour les enseignants"""
    GRADES_CHOICES = [
        ('PA', 'Professeur Assistant'),
        ('MC', 'Maître de Conférences'),
        ('PR', 'Professeur'),
        ('VAC', 'Vacataire'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricule = models.CharField(max_length=20, unique=True)
    grade = models.CharField(max_length=3, choices=GRADES_CHOICES)
    specialite = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True)
    bureau = models.CharField(max_length=20, blank=True)
    modules = models.ManyToManyField(Module, related_name='enseignants', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_grade_display()})"

    @property
    def nom_complet(self):
        return self.user.get_full_name()

class Etudiant(models.Model):
    """Modèle pour les étudiants"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cne = models.CharField(max_length=20, unique=True, verbose_name="CNE")
    cin = models.CharField(max_length=20, unique=True, verbose_name="CIN")
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='etudiants')
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='etudiants')
    date_naissance = models.DateField(verbose_name="Date de naissance")
    lieu_naissance = models.CharField(max_length=100, verbose_name="Lieu de naissance")
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    date_inscription = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Étudiant"
        verbose_name_plural = "Étudiants"
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.filiere.code} {self.niveau}"

    @property
    def nom_complet(self):
        return self.user.get_full_name()

class AlerteSysteme(models.Model):
    """Modèle pour les alertes système"""
    TYPES_CHOICES = [
        ('INFO', 'Information'),
        ('WARNING', 'Avertissement'),
        ('ERROR', 'Erreur'),
        ('SUCCESS', 'Succès'),
    ]
    
    type_alerte = models.CharField(max_length=10, choices=TYPES_CHOICES)
    titre = models.CharField(max_length=100)
    message = models.TextField()
    lu = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Alerte Système"
        verbose_name_plural = "Alertes Système"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_type_alerte_display()} - {self.titre}"

class StatistiqueConnexion(models.Model):
    """Modèle pour les statistiques de connexion"""
    date = models.DateField(unique=True)
    connexions = models.IntegerField(default=0)
    nouveaux_comptes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Statistique de Connexion"
        verbose_name_plural = "Statistiques de Connexion"
        ordering = ['-date']

    def __str__(self):
        return f"Stats {self.date}: {self.connexions} connexions"
