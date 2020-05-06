"""Users app models"""

from django.contrib.auth import get_user_model
from django.db import models


class DeliveryMan(models.Model):
    """Delivery man proxy mode for user"""
    user = models.OneToOneField(
        verbose_name='usuario',
        to=get_user_model(),
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(
        verbose_name='está activo',
        blank=True,
        default=False
    )
    is_available = models.BooleanField(
        verbose_name='está disponible',
        blank=True,
        default=True
    )

    class Meta:
        verbose_name = 'repartidor'
        verbose_name_plural = 'repartidores'