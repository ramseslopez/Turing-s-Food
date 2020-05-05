"""Checkout app utility functions"""


def price_to_cents(price):
    """Returns price in cents"""
    return int(price * 100)
