"""Menu app views"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Item


class ItemListView(LoginRequiredMixin, ListView):
    """Shows all items"""
    model = Item
    template_name = 'menu/list.html'
