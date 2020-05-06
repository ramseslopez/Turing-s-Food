# Generated by Django 3.0.6 on 2020-05-06 09:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_man',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_man_set', to=settings.AUTH_USER_MODEL, verbose_name='repartidor'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Recibido'), (2, 'En Preparación'), (3, 'Listo para ser Recogido'), (4, 'En Camino'), (5, 'Entregado')], default=1, verbose_name='status'),
        ),
    ]
