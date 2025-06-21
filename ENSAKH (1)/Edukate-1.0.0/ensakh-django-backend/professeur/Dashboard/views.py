from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q, F
from django.utils import timezone
from datetime import timedelta
from .models import Module, Grade, Session, Attendance
from .serializers import (
    ModuleSerializer, GradeSerializer, SessionSerializer,
    DashboardStatsSerializer, GradeDistributionSerializer,
    AttendanceStatsSerializer, RecentGradeSerializer,
    UpcomingSessionSerializer
)
from accounts.models import Professor

class ProfessorDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Verify user is a professor
        if not hasattr(request.user, 'professor_profile'):
            return Response(
                {"error": "Accès réservé aux professeurs."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        professor = request.user.professor_profile
        modules = Module.objects.filter(professor=professor)
        
        # Calculate statistics
        nb_modules = modules.count()
        nb_etudiants = StudentModule.objects.filter(module__professor=professor).values('student').distinct().count()
        
        # Calculate percentage of students with at least one grade
        total_students = StudentModule.objects.filter(module__professor=professor).count()
        students_with_grades = StudentModule.objects.filter(
            module__professor=professor,
            grades__isnull=False
        ).distinct().count()
        taux_notes_saisies = (students_with_grades / total_students * 100) if total_students > 0 else 0
        
        # Count sessions this week
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        nb_seances_semaine = Session.objects.filter(
            module__professor=professor,
            date__range=[start_of_week, end_of_week]
        ).count()
        
        stats = {
            'nb_modules': nb_modules,
            'nb_etudiants': nb_etudiants,
            'taux_notes_saisies': round(taux_notes_saisies, 2),
            'nb_seances_semaine': nb_seances_semaine
        }
        
        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)

class GradeDistributionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        professor = request.user.professor_profile
        module_id = request.query_params.get('module_id')
        
        # Base query
        grades = Grade.objects.filter(
            student_module__module__professor=professor
        )
        
        if module_id:
            grades = grades.filter(student_module__module_id=module_id)
        
        # Define grade ranges
        ranges = [
            (0, 5, '0-5'),
            (5, 10, '5-10'),
            (10, 15, '10-15'),
            (15, 20, '15-20'),
        ]
        
        distribution = []
        for min_val, max_val, label in ranges:
            count = grades.filter(
                value__gte=min_val,
                value__lt=max_val
            ).count()
            distribution.append({
                'range_label': label,
                'count': count
            })
        
        serializer = GradeDistributionSerializer(distribution, many=True)
        return Response(serializer.data)

class AttendanceStatsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        professor = request.user.professor_profile
        
        # Get attendance stats for professor's modules
        attendances = Attendance.objects.filter(
            session__module__professor=professor
        )
        
        presents = attendances.filter(status='present').count()
        absents = attendances.filter(status='absent').count()
        
        stats = {
            'presents': presents,
            'absents': absents
        }
        
        serializer = AttendanceStatsSerializer(stats)
        return Response(serializer.data)

class RecentGradesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        professor = request.user.professor_profile
        recent_grades = Grade.objects.filter(
            student_module__module__professor=professor
        ).order_by('-date_created')[:10]
        
        grades_data = []
        for grade in recent_grades:
            grades_data.append({
                'etudiant_nom': f"{grade.student_module.student.user.first_name} {grade.student_module.student.user.last_name}",
                'note': grade.value,
                'type_note': grade.grade_type.name,
                'date_creation': grade.date_created
            })
        
        serializer = RecentGradeSerializer(grades_data, many=True)
        return Response(serializer.data)

class UpcomingSessionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        professor = request.user.professor_profile
        today = timezone.now().date()
        
        upcoming_sessions = Session.objects.filter(
            module__professor=professor,
            date__gte=today
        ).order_by('date', 'start_time')[:10]
        
        sessions_data = []
        for session in upcoming_sessions:
            sessions_data.append({
                'date': session.date,
                'heure_debut': session.start_time,
                'heure_fin': session.end_time,
                'module_nom': session.module.name,
                'salle_nom': session.room
            })
        
        serializer = UpcomingSessionSerializer(sessions_data, many=True)
        return Response(serializer.data)

class ProfessorModulesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ModuleSerializer
    
    def get_queryset):
        professor = self.request.user.professor_profile
        return Module.objects.filter(professor=professor)