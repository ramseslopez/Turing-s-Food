"""Addresses app views"""

from django.conf import settings
from django.views.generic import TemplateView


class AddressCreateView(TemplateView):
    """Adds a new address with Google Maps"""
    template_name = 'addresses/add.html'

    def get_context_data(self, **kwargs):
        """Adds Google Cloud API Key to context"""
        context = super().get_context_data(**kwargs)
        if 'GOOGLE_CLOUD_API_KEY' not in context:
            context['GOOGLE_CLOUD_API_KEY'] = settings.GOOGLE_CLOUD_API_KEY
        return context
