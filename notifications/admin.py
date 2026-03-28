from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'utilisateur', 'type', 'titre', 'est_lu', 'date_creation']  # ← Correction
    list_filter = ['type', 'est_lu', 'date_creation']  # ← Correction
    search_fields = ['titre', 'message', 'utilisateur__email', 'utilisateur__nom']
    readonly_fields = ['date_creation', 'date_lecture']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('utilisateur', 'reservation', 'type', 'titre')
        }),
        ('Contenu', {
            'fields': ('message', 'data')
        }),
        ('Statut de lecture', {
            'fields': ('est_lu', 'date_lecture')
        }),
        ('Dates', {
            'fields': ('date_creation',)
        }),
    )
    
    def mark_as_read(self, request, queryset):
        """Action admin : marquer comme lues"""
        from django.utils import timezone
        queryset.update(est_lu=True, date_lecture=timezone.now())
        self.message_user(request, f"{queryset.count()} notification(s) marquée(s) comme lue(s).")
    
    mark_as_read.short_description = "Marquer comme lues"
    actions = [mark_as_read]