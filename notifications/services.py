from users.models import CustomUser
from .models import Notification


def notifier_reservation_confirmee(reservation):
    passager_user = reservation.passager.utilisateur
    trajet = reservation.trajet
    Notification.objects.create(
        utilisateur=passager_user,
        reservation=reservation,
        type='reservation',
        titre='Réservation confirmée',
        message=(
            f'Votre réservation #{reservation.id} pour {trajet.depart} → {trajet.destination} '
            f'a été confirmée par l\'administrateur.'
        ),
        data={'reservation_id': reservation.id, 'statut': reservation.statut},
    )


def notifier_nouvelle_reservation(reservation):
    """Notifie le passager et tous les administrateurs actifs."""
    trajet = reservation.trajet
    passager_user = reservation.passager.utilisateur

    Notification.objects.create(
        utilisateur=passager_user,
        reservation=reservation,
        type='reservation',
        titre='Réservation enregistrée',
        message=(
            f'Votre demande pour {trajet.depart} → {trajet.destination} '
            f'({reservation.nombre_places} place(s)) est en attente de '
            f'confirmation par un administrateur.'
        ),
        data={'reservation_id': reservation.id, 'statut': reservation.statut},
    )

    for admin in CustomUser.objects.filter(role='admin', is_actif=True):
        Notification.objects.create(
            utilisateur=admin,
            reservation=reservation,
            type='reservation',
            titre='Réservation à confirmer',
            message=(
                f'Réservation #{reservation.id} — '
                f'{passager_user.prenom} {passager_user.nom} : '
                f'{trajet.depart} → {trajet.destination}, '
                f'{reservation.nombre_places} place(s), {reservation.prix_total} FCFA.'
            ),
            data={'reservation_id': reservation.id, 'action': 'confirmer'},
        )
