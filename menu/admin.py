"""Menu app admin site"""

from django.contrib import admin

from .models import Item, ItemSet, ShoppingCart


admin.site.register(Item)
admin.site.register(ItemSet)
admin.site.register(ShoppingCart)
