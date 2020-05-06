"""Addresses app forms"""

from django import forms

from .models import Address


class AddressForm(forms.ModelForm):
    """Form definition for Address."""

    class Meta:
        """Meta definition for Addressform."""
        model = Address
        exclude = ['user', ]

    def save(self, user):
        """Adds user to cleaned data"""
        data = self.cleaned_data
        data['user'] = user
        indoor_number = data.get('indoor_number')
        if not indoor_number:
            data['indoor_number'] = None

        return Address.objects.create(**data)
