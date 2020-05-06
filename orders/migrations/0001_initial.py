# Generated by Django 3.0.6 on 2020-05-06 09:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('addresses', '0006_auto_20200505_2050'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='descripción')),
                ('amount', models.FloatField()),
                ('intent_id', models.CharField(max_length=100, verbose_name='id de intento de stripe')),
                ('status', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Recibido'), (2, 'En Preparación'), (3, 'En Camino'), (4, 'Entregado')], default=1, verbose_name='status')),
                ('ordered_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='addresses.Address', verbose_name='dirección')),
                ('delivery_man', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delivery_man_set', to=settings.AUTH_USER_MODEL, verbose_name='repartidor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_set', to=settings.AUTH_USER_MODEL, verbose_name='usuario')),
            ],
            options={
                'verbose_name': 'orden',
                'verbose_name_plural': 'órdenes',
            },
        ),
    ]