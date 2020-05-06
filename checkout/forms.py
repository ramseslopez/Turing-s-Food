"""Checkout app forms"""

from django import forms

from .models import Order
from menu.models import ShoppingCart


class CheckoutForm(forms.Form):
    """Creates a order"""
    address_id = forms.IntegerField(required=True)
    intent_id = forms.CharField(required=True, max_length=100)

    def save(self, user):
        """Creates description and saves order"""
        data = self.cleaned_data

        shopping_cart = ShoppingCart.objects.get(user=user)
        item_sets = shopping_cart.itemset_set.all()
        data['description'] = ''

        for item_set in item_sets:
            data['description'] += (
                f'{item_set.quantity}x {item_set.item.name}\n'
            )

        data['amount'] = shopping_cart.total
        item_sets.delete()
        shopping_cart.total = 0
        shopping_cart.save()

        return Order.objects.create(user=user, **data)
