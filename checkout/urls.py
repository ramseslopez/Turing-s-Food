"""Checkout app URL config"""

from django.urls import path

from . import views


urlpatterns = [
    path(
        route='',
        view=views.CheckoutView.as_view(),
        name='index'
    ),
    path(
        route='stripe-key',
        view=views.CheckoutClientSecretView.as_view(),
        name='stripe_key'
    ),
]
