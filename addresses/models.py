"""Addresses app models"""

from django.db import models


# class Address(models.Model):
#     """Address model"""
#     street = models.CharField(max_length=255)
#     outdoor_number = models.CharField(max_length=255)
#     indoor_number = models.CharField(max_length=255)
#     suburb = models.CharField(max_length=255)
#     zip_code = models.IntegerField()
#     town = models.CharField(max_length=255)
#     state = models.CharField(max_length=255)
    
# """
# 0 "street_number" (numero)
# 1 "route" (calle)
# 2 "sublocality" (colonia)
# 3 "locality" (ciudad)
# 4 "administrative_area_level_1" (estado)
# 5 "country" (ciudad)
# 6 "postal_code" (zip code)
# """