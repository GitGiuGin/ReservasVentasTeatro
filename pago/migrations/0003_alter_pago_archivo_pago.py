# Generated by Django 5.1.2 on 2024-12-10 05:28

import pago.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pago', '0002_pago_archivo_pago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='archivo_pago',
            field=models.FileField(blank=True, null=True, upload_to=pago.models.renombrar_archivo_pago),
        ),
    ]
