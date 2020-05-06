"""Menu app views"""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, View, CreateView

from .models import Item, ItemSet, ShoppingCart
from .utils import add_item


class ItemListView(LoginRequiredMixin, ListView):
    """Shows all items"""
    model = Item
    template_name = 'menu/items.html'

    def get_queryset(self):
        """Order items"""
        queryset = super().get_queryset()
        queryset = queryset.order_by('name')
        return queryset


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


class AddItemToMenuView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    """Adds item to menu"""
    model = Item
    template_name = 'menu/add.html'
    fields = '__all__'
    success_url = reverse_lazy('menu:items')

    def test_func(self):
        """Checks if user is admin"""
        return self.request.user.status == 3



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


class RemoveItemFromMenuView(UserPassesTestMixin, LoginRequiredMixin, View):
    """Removes a item from menu"""

    def test_func(self):
        """Checks if user is admin"""
        return self.request.user.status == 3

    def post(self, request):
        """Removes item from menu"""
        pk = int(request.POST.get('deleted_item'))
        Item.objects.get(pk=pk).delete()
        return redirect('menu:items')
