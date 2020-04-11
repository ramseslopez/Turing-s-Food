# Generated by Django 3.0.3 on 2020-04-11 04:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core02', '0001_initial'),
        ('core01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.FloatField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('delivered', models.BooleanField(default=False)),
                ('address_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core01.Address')),
                ('delivery_man', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('shoppng_cart_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core03.ShoppingCart')),
            ],
        ),
        migrations.CreateModel(
            name='ItemSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('subtotal', models.FloatField()),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core02.Item')),
                ('shopping_cart_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core03.ShoppingCart')),
            ],
        ),
    ]
