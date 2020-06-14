"""Orders app models"""

from django.contrib.auth import get_user_model
from django.db import models

from addresses.models import Address


class Order(models.Model):
    """Order model"""
    user = models.ForeignKey(
        verbose_name='usuario',
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='user_set'
    )
    description = models.TextField('descripción')
    amount = models.FloatField()
    intent_id = models.CharField('id de intento de stripe', max_length=100)
    address = models.ForeignKey(
        verbose_name='dirección',
        to=Address,
        on_delete=models.CASCADE
    )
    delivery_man = models.ForeignKey(
        verbose_name='repartidor',
        to=get_user_model(),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='delivery_man_set'
    )
    STATUS_CHOICES = (
        (1, 'Recibido'),
        (2, 'En preparación'),
        (3, 'Listo para ser recogido'),
        (4, 'En camino'),
        (5, 'Entregado')
    )
    status = models.PositiveSmallIntegerField(
        verbose_name='status',
        default=1,
        choices=STATUS_CHOICES,
        blank=True
    )
    ordered_at = models.DateTimeField(auto_now_add=True, null=True)
    rating = models.DecimalField(
        verbose_name='calificación',
        max_digits=2,
        decimal_places=1,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'orden'
        verbose_name_plural = 'órdenes'

    def __str__(self):
        return f'Orden #{self.id}'
