from .models import Notification, NotificationType


def notify_payment_validated(paiement):
    user = paiement.reservation.passager.user
    Notification.objects.create(
        user=user,
        type=NotificationType.PAIEMENT,
        message=(
            f"Paiement de {paiement.montant} validé pour la réservation "
            f"#{paiement.reservation_id}."
        ),
    )
