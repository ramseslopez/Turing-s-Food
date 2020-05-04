"""Restautants app forms"""

from django import forms

from slugify import slugify

from .models import Restaurant
from addresses.models import Address


class RestaurantForm(forms.Form):
    """Restaurant form"""
    name = forms.CharField(max_length=255, required=True)
    description = forms.CharField(max_length=255, required=True)
    indoor_number = forms.CharField(max_length=50, required=False)
    logo = forms.ImageField(allow_empty_file=False, required=True)
    latitude = forms.FloatField(required=True)
    longitude = forms.FloatField(required=True)
    address = forms.CharField(max_length=255, required=True)

    def save(self, admin):
        """Saves a restaurant"""
        data = self.cleaned_data

        address_name = data.pop('address')
        indoor_number = data.pop('indoor_number')
        latitude = data.pop('latitude')
        longitude = data.pop('longitude')
        if not indoor_number:
            indoor_number = None

        slug = slugify(data['name'])

        slug_exists = Restaurant.objects.filter(
            slug=slug
        ).exists()
        unique_id = 1

        while slug_exists:
            slug = slugify(data['name'] + ' ' + unique_id)
            unique_id += 1
            slug_exists = Restaurant.objects.filter(
                slug=slug
            ).exists()

        address = Address.objects.create(
            name=address_name,
            indoor_number=indoor_number,
            latitude=latitude,
            longitude=longitude
        )

        return Restaurant.objects.create(
            **data,
            slug=slug,
            address=address,
            admin=admin
        )
