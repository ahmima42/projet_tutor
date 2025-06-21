@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'module', 'date_inscription')
    list_filter = ('module', 'date_inscription')
    search_fields = ('etudiant__user__first_name', 'etudiant__user__last_name', 'module__nom')
    date_hierarchy = 'date_inscription'

@admin.register(Absence)
class AbsenceAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'seance', 'justifie', 'date_absence')
    list_filter = ('justifie', 'seance__date', 'seance__module')
    search_fields = ('etudiant__user__first_name', 'etudiant__user__last_name', 'seance__module__nom')
    date_hierarchy = 'date_absence'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('destinataire', 'message', 'date_notification', 'lue')
    list_filter = ('lue', 'date_notification')
    search_fields = ('destinataire__first_name', 'destinataire__last_name', 'message')
    date_hierarchy = 'date_notification'

@admin.register(Ressource)
class RessourceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'module', 'type_ressource', 'date_publication')
    list_filter = ('type_ressource', 'module', 'date_publication')
    search_fields = ('titre', 'module__nom', 'contenu')
    date_hierarchy = 'date_publication'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('expediteur', 'destinataire', 'sujet', 'date_envoi', 'lu')
    list_filter = ('lu', 'date_envoi')
    search_fields = ('expediteur__first_name', 'expediteur__last_name', 
                    'destinataire__first_name', 'destinataire__last_name', 'sujet')
    date_hierarchy = 'date_envoi'

@admin.register(Devoir)
class DevoirAdmin(admin.ModelAdmin):
    list_display = ('titre', 'module', 'date_publication', 'date_limite')
    list_filter = ('module', 'date_publication')
    search_fields = ('titre', 'module__nom', 'description')
    date_hierarchy = 'date_publication'

@admin.register(Soumission)
class SoumissionAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'devoir', 'date_soumission', 'note')
    list_filter = ('devoir__module', 'date_soumission')
    search_fields = ('etudiant__user__first_name', 'etudiant__user__last_name', 'devoir__titre')
    date_hierarchy = 'date_soumission'

# Configuration de l'interface d'administration
admin.site.site_header = "Administration ENSAKH"
admin.site.site_title = "Portail d'administration ENSAKH"
admin.site.index_title = "Gestion de l'application ENSAKH"