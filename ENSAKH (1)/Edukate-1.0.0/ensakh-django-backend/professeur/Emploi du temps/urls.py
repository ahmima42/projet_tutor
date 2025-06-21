from django.urls import path
from . import views

urlpatterns = [
    path('emploi-du-temps/', views.emploi_du_temps, name='emploi_du_temps'),
]