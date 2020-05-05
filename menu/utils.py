"""Utilitary functions for menu app"""


def add_item(item, item_sets, shopping_cart):
    """Adds a new item to shopping cart"""
    item_set = item_sets.get(item=item)
    item_set.quantity += 1
    item_set.subtotal = item.price * item_set.quantity
    item_set.save()
    shopping_cart.total += item.price
    shopping_cart.save()
