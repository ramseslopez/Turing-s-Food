from django.db import models
from core.models import User


# Create your models here.

class Address(models.Model):
    """ Address model """

    street = models.CharField(max_length=255)
    outdoor_number = models.CharField(max_length=255)
    indoor_number = models.CharField(max_length=255)
    suburb = models.CharField(max_length=255)
    zip_code = models.IntegerField()
    town = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    

class Profile(models.Model):
    """ Profile model """

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)