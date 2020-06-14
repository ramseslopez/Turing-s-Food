"""Checkout app views"""

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, FormView, DetailView

from .forms import CheckoutForm
from orders.models import Order
from .utils import price_to_cents, stripe
from addresses.models import Address


class CheckoutFormView(LoginRequiredMixin, FormView):
    """Checkouts with Stripe"""
    template_name = 'checkout/index.html'
    form_class = CheckoutForm

    def get(self, request, *args, **kwargs):
        item_sets = self.request.user.shoppingcart.total
        if not item_sets:
            return redirect('menu:items')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """Saves order"""
        order = form.save(self.request.user)
        self.success_url = reverse_lazy('checkout:success', args=[order.id, ])
        return super().form_valid(form)

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
        if 'addresses' not in context:
            context['addresses'] = Address.objects.filter(
                user=self.request.user
            )

        return context


class CheckoutSuccessView(LoginRequiredMixin, DetailView):
    """Shows that order is ready"""
    template_name = 'checkout/success.html'
    model = Order

    def get_object(self, queryset=None):
        return get_object_or_404(
            klass=Order,
            pk=self.kwargs.get('pk'),
            user=self.request.user,
            status=1
        )


class CheckoutClientSecretView(LoginRequiredMixin, View):
    """Returns stripe client's secret"""

    def get(self, request):
        """Returns clients_secret"""
        amount = price_to_cents(request.user.shoppingcart.total)
        payment_intent = stripe.create_payment_intent(
            amount=amount,
            customer_id=request.user.customer_id,
            receipt_email=request.user.email
        )
        client_secret = payment_intent.get('client_secret')
        return JsonResponse({'clientSecret': client_secret})


class PayView(LoginRequiredMixin, View):
    """Pays with specified method"""

    def post(self, request):
        """Tooks specified method and pays with it"""
        amount = price_to_cents(request.user.shoppingcart.total)
        intent = stripe.create_payment_intent(
            amount=amount,
            customer_id=request.user.customer_id,
            payment_method=request.POST.get('paymentId'),
            receipt_email=request.user.email
        )
        intent_status = intent.get('status')
        intent_id = intent.get('id')
        data = {
            'status': intent_status,
        }

        if intent_status != 'succeeded':
            data['client_secret'] = intent.get('client_secret')
        else:
            data['id'] = intent_id

        return JsonResponse(data)


class Rating(View):

    template = "rating.html"

    def get(self, request):

        return render(request, self.template)
