from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def approuver_trajets_existants(apps, schema_editor):
    Trajet = apps.get_model('trajets', 'Trajet')
    Trajet.objects.all().update(validation_statut='approuve')


class Migration(migrations.Migration):

    dependencies = [
        ('trajets', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='trajet',
            name='validation_statut',
            field=models.CharField(
                choices=[
                    ('en_attente', 'En attente de validation'),
                    ('approuve', 'Approuvé'),
                    ('rejete', 'Rejeté'),
                ],
                default='en_attente',
                max_length=20,
                verbose_name='Validation admin',
            ),
        ),
        migrations.AddField(
            model_name='trajet',
            name='motif_rejet',
            field=models.TextField(blank=True, verbose_name='Motif de rejet'),
        ),
        migrations.AddField(
            model_name='trajet',
            name='date_validation',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trajet',
            name='valide_par',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='trajets_valides',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddIndex(
            model_name='trajet',
            index=models.Index(fields=['validation_statut'], name='trajets_tra_validat_idx'),
        ),
        migrations.RunPython(approuver_trajets_existants, migrations.RunPython.noop),
    ]
