from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='numero_siege',
            field=models.CharField(
                blank=True,
                help_text='Numéros attribués automatiquement (ex. 3,4,5)',
                max_length=100,
                verbose_name='Siège(s)',
            ),
        ),
    ]
