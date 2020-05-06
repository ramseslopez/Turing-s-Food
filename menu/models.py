"""Menu app models"""

from django.contrib.auth import get_user_model
from django.db import models


class Item(models.Model):
    """Menu item"""
    name = models.CharField('nombre', max_length=100)
    image = models.ImageField('imagen', upload_to='items')
    description = models.CharField('descripción', max_length=255)
    price = models.FloatField('precio')

    class Meta:
        verbose_name = 'artículo'

    def __str__(self):
        """Returns string representation of a item"""
        return f'{self.name}'


class ItemSetManager(models.Manager):
    """Adds creation functionality"""

    def create_itemset(self, item, shopping_cart):
        """Dinamically sets quantity and price"""
        shopping_cart.total += item.price
        shopping_cart.save()
        return self.create(
            item=item,
            shopping_cart=shopping_cart,
            quantity=1,
            subtotal=item.price
        )


class ItemSet(models.Model):
    """Item set model"""
    item = models.ForeignKey(
        verbose_name='artículo',
        to=Item,
        on_delete=models.CASCADE
    )
    shopping_cart = models.ForeignKey(
        verbose_name='carrito de compras',
        to='ShoppingCart',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField('cantidad')
    subtotal = models.FloatField('subtotal')
    objects = ItemSetManager()

    class Meta:
        verbose_name = 'conjunto de artículos'
        verbose_name_plural = 'conjuntos de artículos'

    def __str__(self):
        """Returns string representation of a item set"""
        return (
            f'{self.quantity}x {self.item.name} '
            f'({self.shopping_cart.user.email})'
        )


class ShoppingCart(models.Model):
    """Shopping cart model"""
    user = models.OneToOneField(
        verbose_name='usuario',
        to=get_user_model(),
        on_delete=models.CASCADE
    )
    total = models.FloatField('total', blank=True, default=0)

    class Meta:
        verbose_name = 'carrito de compras'
        verbose_name_plural = 'carritos de compras'

    def __str__(self):
        """Returns string representation of a shopping cart"""
        return f'Carrito de {self.user.email}'
