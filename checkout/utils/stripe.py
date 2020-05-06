"""Stripe checkout utilities"""

from django.conf import settings

import stripe


stripe.api_key = settings.STRIPE_API_KEY


def create_customer():
    """Returns a stripe customer"""
    return stripe.Customer.create()


def create_payment_intent(amount, customer_id, payment_method=None):
    """
    Creates a payment intent. If payment method is provided, it uses it
    """

    if not payment_method:
        return stripe.PaymentIntent.create(
            amount=amount,
            currency='mxn',
            customer=customer_id,
        )
    else:
        try:
            return stripe.PaymentIntent.create(
                amount=amount,
                currency='mxn',
                customer=customer_id,
                payment_method=payment_method,
                off_session=True,
                confirm=True,
            )
        except stripe.error.CardError as e:
            err = e.error
            payment_intent_id = err.payment_intent['id']
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return payment_intent


def list_payment_methods(customer_id):
    """Lists saved cards"""
    return stripe.PaymentMethod.list(
        customer=customer_id,
        type="card",
    )


