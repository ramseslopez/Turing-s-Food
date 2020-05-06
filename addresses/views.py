"""Addresses app views"""

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import AddressForm
from .models import Address


class AddressCreateView(LoginRequiredMixin, FormView):
    """Adds a new user address with Google Maps APIs"""
    template_name = 'addresses/add.html'
    form_class = AddressForm
    success_url = reverse_lazy('menu:items')

    def get_context_data(self, **kwargs):
        """Adds Google Cloud API Key to context"""
        context = super().get_context_data(**kwargs)
        if 'GOOGLE_CLOUD_API_KEY' not in context:
            context['GOOGLE_CLOUD_API_KEY'] = settings.GOOGLE_CLOUD_API_KEY
        return context

    def form_valid(self, form):
        """Checks if user has not address with form alias, and saves model"""
        alias = form.cleaned_data.get('alias')
        user = self.request.user
        alias_exists = Address.objects.filter(
            alias=alias,
            user=user
        ).exists()
        if alias_exists:
            form.add_error(
                field='alias',
                error=f'Ya cuentas con una dirección con el alias "{alias}"'
            )
            return super().form_invalid(form)

        address = form.save(user)
        next = self.request.GET.get('next')
        if next:
            next += f'?address={address.pk}'
            self.success_url = next

        return super().form_valid(form)
