"""Menu app views"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import ListView, View

from .models import Item, ItemSet, ShoppingCart
from .utils import add_item


class ItemListView(LoginRequiredMixin, ListView):
    """Shows all items"""
    model = Item
    template_name = 'menu/items.html'


class CartView(LoginRequiredMixin, ListView):
    """Shows all cart items"""
    model = ItemSet
    template_name = 'menu/cart.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        shopping_cart = self.request.user.shoppingcart
        queryset = queryset.filter(shopping_cart=shopping_cart)
        return queryset


class AddItemToCartView(LoginRequiredMixin, View):
    """Adds a item to user's cart"""

    def post(self, request):
        """Adds a item to user's shopping cart"""
        pk = int(request.POST.get('id'))
        item = Item.objects.get(pk=pk)
        shopping_cart = ShoppingCart.objects.get(user=request.user)
        item_sets = shopping_cart.itemset_set.all()
        item_already_in = item_sets.filter(item=item).exists()
        if item_already_in:
            add_item(item, item_sets, shopping_cart)
        else:
            ItemSet.objects.create_itemset(item, shopping_cart)
        return JsonResponse({
            'count': item_sets.count(),
            'message': f'{item.name} agregado al carrito.',
        })


class RemoveItemFromCartView(LoginRequiredMixin, View):
    """Removes a item set to user's cart"""

    def post(self, request):
        """Adds a item to user's shopping cart"""
        pk = int(request.POST.get('id'))
        item_set = ItemSet.objects.get(pk=pk)
        shopping_cart = ShoppingCart.objects.get(user=request.user)
        subtotal = item_set.subtotal
        item_set.delete()
        shopping_cart.total -= subtotal
        shopping_cart.save()
        return JsonResponse({
            'count': shopping_cart.itemset_set.count(),
            'message': (
                f'{item_set.quantity}x {item_set.item.name} '
                'ha sido eliminado del carrito.'
            ),
            'total': shopping_cart.total
        })
