"""Addresses app forms"""

from django import forms

from .models import UserAddress


class AddressForm(forms.ModelForm):
    """Form definition for Address."""

    class Meta:
        """Meta definition for Addressform."""
        model = UserAddress
        exclude = ['user', ]

    def save(self, user):
        """Adds user to cleaned data"""
        data = self.cleaned_data
        data['user'] = user
        indoor_number = data.get('indoor_number')
        if not indoor_number:
            data['indoor_number'] = None

        return UserAddress.objects.create(**data)
