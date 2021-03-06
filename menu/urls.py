"""Menu URL config"""

from django.urls import path

from . import views


urlpatterns = [
    path('', views.ItemListView.as_view(), name='items'),
    path('cart', views.CartView.as_view(), name='cart'),
    path('add-to-cart', views.AddItemToCartView.as_view(), name='add_to_cart'),
    path(
        route='remove-from-cart',
        view=views.RemoveItemFromCartView.as_view(),
        name='remove_from_cart'
    ),
    path(
        route='add-to-menu',
        view=views.AddItemToMenuView.as_view(),
        name='add_to_menu'
    ),
    path(
        route='update/<int:pk>',
        view=views.ItemUpdateView.as_view(),
        name='update_item'
    ),
    path(
        route='remove-from-menu',
        view=views.RemoveItemFromMenuView.as_view(),
        name='remove_from_menu'
    ),
]
