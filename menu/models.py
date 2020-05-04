"""Restaurants app models"""

from django.contrib.auth import get_user_model
from django.db import models

from addresses.models import Address


class Item(models.Model):
    """Restaurant item"""
    name = models.CharField('nombre', max_length=100)
    image = models.ImageField('imagen', upload_to='items')
    description = models.CharField('descripción', max_length=255)
    price = models.FloatField('precio')

    class Meta:
        verbose_name = 'artículo'

    def __str__(self):
        """Returns string representation of a item"""
        return f'{self.name} de {self.restaurant.name}'
