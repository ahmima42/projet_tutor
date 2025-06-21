from rest_framework import serializers
from .models import Module, StudentModule, Grade, GradeType, Session, Attendance
from accounts.serializers import StudentProfileSerializer

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'

class StudentModuleSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer()
    module = ModuleSerializer()
    
    class Meta:
        model = StudentModule
        fields = '__all__'

class GradeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeType
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    student_module = StudentModuleSerializer()
    grade_type = GradeTypeSerializer()
    
    class Meta:
        model = Grade
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    module = ModuleSerializer()
    
    class Meta:
        model = Session
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    session = SessionSerializer()
    student = StudentProfileSerializer()
    
    class Meta:
        model = Attendance
        fields = '__all__'

class DashboardStatsSerializer(serializers.Serializer):
    nb_modules = serializers.IntegerField()
    nb_etudiants = serializers.IntegerField()
    taux_notes_saisies = serializers.DecimalField(max_digits=5, decimal_places=2)
    nb_seances_semaine = serializers.IntegerField()

class GradeDistributionSerializer(serializers.Serializer):
    range_label = serializers.CharField()
    count = serializers.IntegerField()

class AttendanceStatsSerializer(serializers.Serializer):
    presents = serializers.IntegerField()
    absents = serializers.IntegerField()

class RecentGradeSerializer(serializers.Serializer):
    etudiant_nom = serializers.CharField()
    note = serializers.DecimalField(max_digits=5, decimal_places=2)
    type_note = serializers.CharField()
    date_creation = serializers.DateTimeField()

class UpcomingSessionSerializer(serializers.Serializer):
    date = serializers.DateField()
    heure_debut = serializers.TimeField()
    heure_fin = serializers.TimeField()
    module_nom = serializers.CharField()
    salle_nom = serializers.CharField()