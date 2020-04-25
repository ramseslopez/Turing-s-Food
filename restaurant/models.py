from django.db import models
from core.models import User
from info_user.models import Address

# Create your models here.

class Restaurant(models.Model):
    """ Restaurant model """

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class Menu(models.Model):
    """ Menu model """

    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)


class Item(models.Model):
    """ Item model """

    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    #image = models.ImageField(upload_to="images")
    description = models.CharField(max_length=255)
    price = models.FloatField()
