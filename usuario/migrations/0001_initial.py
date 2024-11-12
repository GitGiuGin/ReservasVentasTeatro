# Generated by Django 5.1.1 on 2024-10-08 15:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefono', models.CharField(blank=True, max_length=15, verbose_name='Teléfono')),
                ('direccion', models.CharField(blank=True, max_length=255, verbose_name='Dirección')),
                ('tipo_usuario', models.CharField(choices=[('cliente', 'Cliente'), ('personal', 'Personal de Trabajo')], default='cliente', max_length=10, verbose_name='Tipo de Usuario')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
                'db_table': 'usuario',
            },
        ),
    ]
