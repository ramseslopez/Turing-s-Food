"""Addresses app admin site"""

from django.contrib import admin

from .models import Address


admin.site.register(Address)
