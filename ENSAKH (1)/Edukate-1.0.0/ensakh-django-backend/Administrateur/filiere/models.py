from django.db import models

class Filiere(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom de la filière")
    code = models.CharField(max_length=10, unique=True, verbose_name="Code")
    description = models.TextField(verbose_name="Description")
    responsable = models.CharField(max_length=100, verbose_name="Responsable")
    couleur_primaire = models.CharField(max_length=7, default="#667eea", verbose_name="Couleur primaire")
    couleur_secondaire = models.CharField(max_length=7, default="#764ba2", verbose_name="Couleur secondaire")
    duree_annees = models.IntegerField(default=3, verbose_name="Durée en années")
    capacite_max = models.IntegerField(verbose_name="Capacité maximale")
    statut = models.CharField(
        max_length=10,
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        default='active',
        verbose_name="Statut"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Filière"
        verbose_name_plural = "Filières"
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.nom}"

    @property
    def nb_etudiants(self):
        # Simulation du nombre d'étudiants
        return {
            'GI': 350,
            'GIID': 250,
            'MGSI': 40,
            'GE': 180,
            'GP': 120,
        }.get(self.code, 0)

    @property
    def nb_modules(self):
        # Simulation du nombre de modules
        return {
            'GI': 18,
            'GIID': 16,
            'MGSI': 14,
            'GE': 15,
            'GP': 12,
        }.get(self.code, 0)

    @property
    def nb_enseignants(self):
        # Simulation du nombre d'enseignants
        return {
            'GI': 12,
            'GIID': 10,
            'MGSI': 8,
            'GE': 9,
            'GP': 6,
        }.get(self.code, 0)

    @property
    def gradient_style(self):
        return f"background: linear-gradient(135deg, {self.couleur_primaire} 0%, {self.couleur_secondaire} 100%);"

class Niveau(models.Model):
    nom = models.CharField(max_length=50, verbose_name="Nom du niveau")
    code = models.CharField(max_length=5, unique=True, verbose_name="Code")
    ordre = models.IntegerField(verbose_name="Ordre")
    semestre1 = models.CharField(max_length=20, verbose_name="Premier semestre")
    semestre2 = models.CharField(max_length=20, verbose_name="Deuxième semestre")
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Niveau"
        verbose_name_plural = "Niveaux"
        ordering = ['ordre']

    def __str__(self):
        return f"{self.code} - {self.nom}"

    @property
    def nb_etudiants(self):
        # Simulation du nombre d'étudiants par niveau
        return {
            '1A': 450,
            '2A': 380,
            '3A': 320,
            '4A': 250,
        }.get(self.code, 0)

    @property
    def nb_modules(self):
        # Simulation du nombre de modules par niveau
        return {
            '1A': 12,
            '2A': 14,
            '3A': 16,
            '4A': 10,
        }.get(self.code, 0)
