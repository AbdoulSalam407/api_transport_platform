from django.db.models.signals import post_save
from django.dispatch import receiver

from reservations.models import Reservation

from .services import notifier_nouvelle_reservation


@receiver(post_save, sender=Reservation)
def reservation_creee(sender, instance, created, **kwargs):
    if created and instance.statut == 'en_attente':
        notifier_nouvelle_reservation(instance)
