"""Users app admin site"""

from django.contrib import admin

from .models import DeliveryMan


admin.site.register(DeliveryMan)
