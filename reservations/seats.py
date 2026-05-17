"""Attribution automatique des sièges pour les réservations."""

from __future__ import annotations

from .models import Reservation


def parse_sieges(numero_siege: str) -> list[str]:
    if not numero_siege:
        return []
    return [s.strip() for s in numero_siege.split(',') if s.strip()]


def format_sieges(sieges: list[str]) -> str:
    return ','.join(sieges)


def sieges_occupes(trajet, exclude_reservation_id=None) -> set[str]:
    """Sièges déjà pris sur un trajet (réservations en attente ou confirmées)."""
    qs = Reservation.objects.filter(
        trajet=trajet,
        statut__in=['en_attente', 'confirmee'],
    )
    if exclude_reservation_id:
        qs = qs.exclude(pk=exclude_reservation_id)

    occupes: set[str] = set()
    for reservation in qs:
        occupes.update(parse_sieges(reservation.numero_siege))
    return occupes


def _ordre_selon_preference(capacite: int, preference: str) -> list[str]:
    """Ordre de priorité des numéros de siège (1 … capacité)."""
    tous = [str(i) for i in range(1, capacite + 1)]
    impairs = [s for s in tous if int(s) % 2 == 1]
    pairs = [s for s in tous if int(s) % 2 == 0]

    if preference == 'fenetre':
        return impairs + pairs
    if preference == 'couloir':
        return pairs + impairs
    return tous


def _bloc_consecutif_libre(capacite: int, occupes: set[str], nombre: int) -> list[str] | None:
    """Cherche un bloc de sièges numérotés consécutifs (ex. 3,4,5)."""
    occ_int = {int(s) for s in occupes if s.isdigit()}
    for start in range(1, capacite - nombre + 2):
        bloc = list(range(start, start + nombre))
        if all(n not in occ_int for n in bloc):
            return [str(n) for n in bloc]
    return None


def attribuer_sieges_automatiquement(trajet, nombre_places: int, passager=None) -> str:
    """
    Attribue automatiquement des sièges libres.
    Tient compte des préférences passager (fenêtre / couloir / indifférent).
    """
    if nombre_places < 1:
        raise ValueError('Le nombre de places doit être au moins 1.')

    capacite = trajet.places_totales
    if nombre_places > capacite:
        raise ValueError('Nombre de places demandé supérieur à la capacité du véhicule.')

    occupes = sieges_occupes(trajet)
    libres_total = capacite - len(occupes)
    if libres_total < nombre_places:
        raise ValueError('Pas assez de sièges libres sur ce trajet.')

    preference = 'indifferent'
    if passager is not None:
        preference = getattr(passager, 'preferences_siege', 'indifferent') or 'indifferent'

    if nombre_places > 1:
        bloc = _bloc_consecutif_libre(capacite, occupes, nombre_places)
        if bloc:
            return format_sieges(bloc)

    ordre = _ordre_selon_preference(capacite, preference)
    attribues: list[str] = []
    for siege in ordre:
        if siege not in occupes and siege not in attribues:
            attribues.append(siege)
            if len(attribues) == nombre_places:
                return format_sieges(attribues)

    raise ValueError('Impossible d\'attribuer des sièges automatiquement.')
