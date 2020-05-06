# Generated by Django 3.0.6 on 2020-05-06 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'orden', 'verbose_name_plural': 'órdenes'},
        ),
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]