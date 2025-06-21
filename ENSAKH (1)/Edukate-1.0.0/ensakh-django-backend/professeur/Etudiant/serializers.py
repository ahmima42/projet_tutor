from rest_framework import serializers
from .models import Etudiant, Note, Module

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'nom', 'code']

class NoteSerializer(serializers.ModelSerializer):
    module = ModuleSerializer()
    
    class Meta:
        model = Note
        fields = ['id', 'module', 'valeur', 'date_evaluation', 'remarque']

class EtudiantSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    niveau = serializers.StringRelatedField()
    
    class Meta:
        model = Etudiant
        fields = ['id', 'cne', 'full_name', 'niveau', 'telephone', 'photo']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()