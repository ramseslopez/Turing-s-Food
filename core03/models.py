from django.db import models
from core.models import User
from core02.models import Item
from core01.models import Address

# Create your models here.

class ShoppingCart(models.Model):
    """ Shopping cart models """

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()


class ItemSet(models.Model):
    """ Item set model """

    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    shopping_cart_id = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    subtotal = models.FloatField()


class Order(models.Model):
    """ Order model """

    shoppng_cart_id = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)
    delivery_man = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True, null=True)
    delivered = models.BooleanField(default=False)