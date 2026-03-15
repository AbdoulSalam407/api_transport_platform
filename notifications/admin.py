from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("titre", "utilisateur", "type_notification", "is_read", "date_creation")
    list_filter = ("type_notification", "is_read", "date_creation")
    search_fields = ("titre", "message", "utilisateur__username")
    readonly_fields = ("date_creation", "date_lecture")
