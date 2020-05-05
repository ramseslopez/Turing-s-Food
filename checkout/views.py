"""Checkout app views"""

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import View, TemplateView

from .utils import price_to_cents, stripe


class CheckoutView(TemplateView):
    """Checkouts with Stripe"""
    template_name = 'checkout/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'STRIPE_PUBLISHABLE_KEY' not in context:
            context['STRIPE_PUBLISHABLE_KEY'] = (
                settings.STRIPE_PUBLISHABLE_KEY
            )
        if 'amount' not in context:
            context['amount'] = 10000
        if 'payment_methods' not in context:
            payment_methods = stripe.list_payment_methods(
                customer_id=self.request.user.customer_id
            )
            context['payment_methods'] = payment_methods

        return context


class CheckoutClientSecretView(LoginRequiredMixin, View):
    """Returns stripe client's secret"""

    def get(self, request):
        """Returns clients_secret"""
        amount = price_to_cents(request.user.shoppingcart.total)
        payment_intent = stripe.create_payment_intent(
            amount=amount,
            customer_id=request.user.customer_id
        )
        client_secret = payment_intent.get('client_secret')
        return JsonResponse({'clientSecret': client_secret})
