from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("client", "trajet", "nombre_places", "prix_total", "status", "date_reservation")
    list_filter = ("status", "date_reservation")
    search_fields = ("client__username", "trajet__depart")
    readonly_fields = ("date_reservation", "date_modification")
