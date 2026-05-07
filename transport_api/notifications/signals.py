from django.db.models.signals import post_save
from django.dispatch import receiver

from reservations.models import Reservation

from .models import Notification, NotificationType


@receiver(post_save, sender=Reservation)
def notify_after_reservation(sender, instance: Reservation, created, **kwargs):
    if not created:
        return
    user = instance.passager.user
    Notification.objects.create(
        user=user,
        type=NotificationType.RESERVATION,
        message=(
            f"Votre réservation #{instance.pk} pour le trajet "
            f"{instance.trajet.ville_depart} → {instance.trajet.ville_arrivee} "
            f"a été enregistrée ({instance.nombre_places} place(s))."
        ),
    )
