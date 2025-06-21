from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Filiere, Niveau, Module, Etudiant, Note

class EtudiantInline(admin.StackedInline):
    model = Etudiant
    can_delete = False
    verbose_name_plural = 'Étudiants'

class CustomUserAdmin(UserAdmin):
    inlines = (EtudiantInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class NoteInline(admin.TabularInline):
    model = Note
    extra = 1

@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ('nom', 'filiere')
    list_filter = ('filiere',)
    search_fields = ('nom', 'filiere__nom')

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code', 'niveau', 'professeur')
    list_filter = ('niveau', 'professeur')
    search_fields = ('nom', 'code')
    inlines = [NoteInline]

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('user', 'cne', 'niveau', 'date_inscription')
    list_filter = ('niveau', 'date_inscription')
    search_fields = ('user__first_name', 'user__last_name', 'cne')
    raw_id_fields = ('user',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'module', 'valeur', 'date_evaluation')
    list_filter = ('module', 'date_evaluation')
    search_fields = ('etudiant__user__first_name', 'etudiant__user__last_name', 'module__nom')