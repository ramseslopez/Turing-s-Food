"""Addresses app URL config"""

from django.urls import path

from . import views


urlpatterns = [
    path('add', views.AddressCreateView.as_view(), name='add'),
]
