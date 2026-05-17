from django.db import migrations


def corriger_places_disponibles(apps, schema_editor):
    Trajet = apps.get_model('trajets', 'Trajet')
    Reservation = apps.get_model('reservations', 'Reservation')
    for trajet in Trajet.objects.filter(places_disponibles=0, places_totales__gt=0):
        places_reservees = sum(
            Reservation.objects.filter(
                trajet_id=trajet.pk,
                statut__in=['en_attente', 'confirmee'],
            ).values_list('nombre_places', flat=True)
        )
        if places_reservees > 0:
            continue
        trajet.places_disponibles = trajet.places_totales
        if trajet.statut == 'complet':
            trajet.statut = 'actif'
        trajet.save(update_fields=['places_disponibles', 'statut'])


class Migration(migrations.Migration):

    dependencies = [
        ('trajets', '0004_rename_trajets_tra_validat_idx_trajets_tra_validat_8096b0_idx'),
    ]

    operations = [
        migrations.RunPython(corriger_places_disponibles, migrations.RunPython.noop),
    ]
