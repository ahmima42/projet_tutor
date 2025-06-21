from django.urls import path
from .views import (
    ProfessorDashboardView, GradeDistributionView,
    AttendanceStatsView, RecentGradesView,
    UpcomingSessionsView, ProfessorModulesView
)

urlpatterns = [
    path('stats/', ProfessorDashboardView.as_view(), name='professor-dashboard'),
    path('grades-distribution/', GradeDistributionView.as_view(), name='grades-distribution'),
    path('attendance-stats/', AttendanceStatsView.as_view(), name='attendance-stats'),
    path('recent-grades/', RecentGradesView.as_view(), name='recent-grades'),
    path('upcoming-sessions/', UpcomingSessionsView.as_view(), name='upcoming-sessions'),
    path('modules/', ProfessorModulesView.as_view(), name='professor-modules'),
]