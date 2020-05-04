"""Restaurants app views"""

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView

from .models import Restaurant
from .forms import RestaurantForm


class RestaurantListView(LoginRequiredMixin, ListView):
    """Shows all restaurants"""
    model = Restaurant
    template_name = 'restaurants/list.html'


class RestaurantDetailView(LoginRequiredMixin, DetailView):
    """Shows menu or administrator view"""
    model = Restaurant
    template_name = 'restaurants/detail.html'


class RestaurantFormView(LoginRequiredMixin, FormView):
    """Creates a new restaurant"""
    template_name = 'restaurants/create.html'
    form_class = RestaurantForm

    def get_context_data(self, **kwargs):
        """Adds Google Cloud API Key to context"""
        context = super().get_context_data(**kwargs)
        if 'GOOGLE_CLOUD_API_KEY' not in context:
            context['GOOGLE_CLOUD_API_KEY'] = settings.GOOGLE_CLOUD_API_KEY
        return context

    def form_valid(self, form):
        """Saves a restaurant and adds success url"""
        restaurant = form.save(self.request.user)
        self.success_url = success_url = reverse_lazy(
            viewname='restaurants:detail',
            args=[restaurant.slug]
        )
        return super().form_valid(form)
