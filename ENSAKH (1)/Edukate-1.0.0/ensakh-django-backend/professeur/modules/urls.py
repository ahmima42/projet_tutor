from django.urls import path
from . import views

urlpatterns = [
    path('mes-modules/', views.mes_modules, name='mes_modules'),
    path('module/<int:module_id>/', views.details_module, name='details_module'),
]