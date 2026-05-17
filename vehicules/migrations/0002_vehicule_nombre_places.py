from django.db import migrations, models


def copier_places_modele(apps, schema_editor):
    Vehicule = apps.get_model('vehicules', 'Vehicule')
    for vehicule in Vehicule.objects.select_related('modele').all():
        if not vehicule.nombre_places and vehicule.modele_id:
            vehicule.nombre_places = vehicule.modele.nombre_places
            vehicule.save(update_fields=['nombre_places'])


class Migration(migrations.Migration):

    dependencies = [
        ('vehicules', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicule',
            name='nombre_places',
            field=models.PositiveIntegerField(
                blank=True,
                help_text='Capacité réelle du véhicule (si différente du modèle).',
                null=True,
                verbose_name='Nombre de places passagers',
            ),
        ),
        migrations.RunPython(copier_places_modele, migrations.RunPython.noop),
    ]
