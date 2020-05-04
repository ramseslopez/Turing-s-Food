"""Restaurants app models"""

from django.contrib.auth import get_user_model
from django.db import models

from addresses.models import Address


class Restaurant(models.Model):
    """ Restaurant model """
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos')
    description = models.CharField(max_length=255)
    admin = models.ForeignKey(
        verbose_name='administrador',
        to=get_user_model(),
        on_delete=models.CASCADE
    )
    address = models.ForeignKey(
        verbose_name='dirección',
        to=Address,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'restaurante'

    def __str__(self):
        """Returns string representation of restaurant"""
        return self.name


class Item(models.Model):
    """Restaurant item"""
    name = models.CharField('nombre', max_length=100)
    restaurant = models.ForeignKey(
        verbose_name='restaurante',
        to='Restaurant',
        on_delete=models.CASCADE
    )
    image = models.ImageField('imagen', upload_to='items')
    description = models.CharField('descripción', max_length=255)
    price = models.FloatField('precio')

    class Meta:
        verbose_name = 'artículo'

    def __str__(self):
        """Returns string representation of a item"""
        return f'{self.name} de {self.restaurant.name}'
