# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import *

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class ProfesseurForm(forms.ModelForm):
    class Meta:
        model = Professeur
        fields = ['matricule', 'specialite', 'grade']
        widgets = {
            'matricule': forms.TextInput(attrs={'class': 'form-control'}),
            'specialite': forms.TextInput(attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['numero_etudiant', 'filiere', 'niveau', 'date_naissance', 'lieu_naissance']
        widgets = {
            'numero_etudiant': forms.TextInput(attrs={'class': 'form-control'}),
            'filiere': forms.Select(attrs={'class': 'form-control'}),
            'niveau': forms.Select(attrs={'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lieu_naissance': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['nom', 'code', 'description', 'coefficient', 'heures_cours', 'heures_td', 'heures_tp', 'filiere', 'niveau', 'semestre']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'coefficient': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'heures_cours': forms.NumberInput(attrs={'class': 'form-control'}),
            'heures_td': forms.NumberInput(attrs={'class': 'form-control'}),
            'heures_tp': forms.NumberInput(attrs={'class': 'form-control'}),
            'filiere': forms.Select(attrs={'class': 'form-control'}),
            'niveau': forms.Select(attrs={'class': 'form-control'}),
            'semestre': forms.Select(attrs={'class': 'form-control'}),
        }

class SeanceForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = ['module', 'type_seance', 'titre', 'description', 'date', 'heure_debut', 'heure_fin', 'salle']
        widgets = {
            'module': forms.Select(attrs={'class': 'form-control'}),
            'type_seance': forms.Select(attrs={'class': 'form-control'}),
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'heure_debut': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'heure_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'salle': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        heure_debut = cleaned_data.get('heure_debut')
        heure_fin = cleaned_data.get('heure_fin')
        
        if heure_debut and heure_fin:
            if heure_debut >= heure_fin:
                raise ValidationError("L'heure de fin doit être postérieure à l'heure de début.")
        
        return cleaned_data

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['type_evaluation', 'note', 'coefficient', 'date_evaluation', 'commentaire']
        widgets = {
            'type_evaluation': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.25', 'min': '0', 'max': '20'}),
            'coefficient': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0.5'}),
            'date_evaluation': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
    
    def clean_note(self):
        note = self.cleaned_data['note']
        if note < 0 or note > 20:
            raise ValidationError("La note doit être comprise entre 0 et 20.")
        return note

class PresenceForm(forms.ModelForm):
    class Meta:
        model = Presence
        fields = ['present', 'retard', 'justifie', 'commentaire']
        widgets = {
            'present': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'retard': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'justifie': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class FiltreEtudiantForm(forms.Form):
    filiere = forms.ModelChoiceField(
        queryset=Filiere.objects.all(),
        required=False,
        empty_label="Toutes les filières",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    niveau = forms.ModelChoiceField(
        queryset=Niveau.objects.all(),
        required=False,
        empty_label="Tous les niveaux",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rechercher...'})
    )

# serializers.py
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_type']

class FiliereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filiere
        fields = '__all__'

class NiveauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Niveau
        fields = '__all__'

class SemestreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semestre
        fields = '__all__'

class ProfesseurSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Professeur
        fields = '__all__'

class EtudiantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    filiere = FiliereSerializer(read_only=True)
    niveau = NiveauSerializer(read_only=True)
    
    class Meta:
        model = Etudiant
        fields = '__all__'

class ModuleSerializer(serializers.ModelSerializer):
    professeur = ProfesseurSerializer(read_only=True)
    filiere = FiliereSerializer(read_only=True)
    niveau = NiveauSerializer(read_only=True)
    semestre = SemestreSerializer(read_only=True)
    
    class Meta:
        model = Module
        fields = '__all__'

class SalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salle
        fields = '__all__'

class SeanceSerializer(serializers.ModelSerializer):
    module = ModuleSerializer(read_only=True)
    salle = SalleSerializer(read_only=True)
    
    class Meta:
        model = Seance
        fields = '__all__'

class InscriptionSerializer(serializers.ModelSerializer):
    etudiant = EtudiantSerializer(read_only=True)
    module = ModuleSerializer(read_only=True)
    semestre = SemestreSerializer(read_only=True)
    
    class Meta:
        model = Inscription
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):
    inscription = InscriptionSerializer(read_only=True)
    
    class Meta:
        model = Note
        fields = '__all__'

class PresenceSerializer(serializers.ModelSerializer):
    etudiant = EtudiantSerializer(read_only=True)
    seance = SeanceSerializer(read_only=True)
    
    class Meta:
        model = Presence
        fields = '__all__'

# API ViewSets
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Avg

class ModuleViewSet(viewsets.ModelViewSet):
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type == 'professeur':
            return Module.objects.filter(professeur__user=self.request.user)
        elif self.request.user.user_type == 'etudiant':
            return Module.objects.filter(inscription__etudiant__user=self.request.user)
        return Module.objects.all()
    
    @action(detail=True, methods=['get'])
    def etudiants(self, request, pk=None):
        module = self.get_object()
        inscriptions = Inscription.objects.filter(module=module)
        serializer = InscriptionSerializer(inscriptions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def seances(self, request, pk=None):
        module = self.get_object()
        seances = Seance.objects.filter(module=module).order_by('-date', '-heure_debut')
        serializer = SeanceSerializer(seances, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def notes(self, request, pk=None):
        module = self.get_object()
        notes = Note.objects.filter(inscription__module=module)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

class EtudiantViewSet(viewsets.ModelViewSet):
    serializer_class = EtudiantSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type == 'professeur':
            # Étudiants des modules du professeur
            return Etudiant.objects.filter(
                inscription__module__professeur__user=self.request.user
            ).distinct()
        elif self.request.user.user_type == 'etudiant':
            # Seulement l'étudiant connecté
            return Etudiant.objects.filter(user=self.request.user)
        return Etudiant.objects.all()
    
    @action(detail=True, methods=['get'])
    def modules(self, request, pk=None):
        etudiant = self.get_object()
        inscriptions = Inscription.objects.filter(etudiant=etudiant)
        serializer = InscriptionSerializer(inscriptions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def notes(self, request, pk=None):
        etudiant = self.get_object()
        notes = Note.objects.filter(inscription__etudiant=etudiant)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

class SeanceViewSet(viewsets.ModelViewSet):
    serializer_class = SeanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type == 'professeur':
            return Seance.objects.filter(module__professeur__user=self.request.user)
        elif self.request.user.user_type == 'etudiant':
            return Seance.objects.filter(module__inscription__etudiant__user=self.request.user)
        return Seance.objects.all()
    
    @action(detail=True, methods=['get', 'post'])
    def presences(self, request, pk=None):
        seance = self.get_object()
        
        if request.method == 'GET':
            presences = Presence.objects.filter(seance=seance)
            serializer = PresenceSerializer(presences, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            # Saisie des présences
            presences_data = request.data.get('presences', [])
            for presence_data in presences_data:
                etudiant_id = presence_data.get('etudiant_id')
                try:
                    etudiant = Etudiant.objects.get(id=etudiant_id)
                    Presence.objects.update_or_create(
                        etudiant=etudiant,
                        seance=seance,
                        defaults={
                            'present': presence_data.get('present', False),
                            'retard': presence_data.get('retard', False),
                            'justifie': presence_data.get('justifie', False),
                            'commentaire': presence_data.get('commentaire', ''),
                        }
                    )
                except Etudiant.DoesNotExist:
                    continue
            
            return Response({'message': 'Présences enregistrées avec succès'})

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type == 'professeur':
            return Note.objects.filter(inscription__module__professeur__user=self.request.user)
        elif self.request.user.user_type == 'etudiant':
            return Note.objects.filter(inscription__etudiant__user=self.request.user)
        return Note.objects.all()