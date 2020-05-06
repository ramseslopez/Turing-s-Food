"""turing_food URL Configuration"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('menu.urls', 'menu'), namespace='menu')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path(
        route='addresses/',
        view=include(('addresses.urls', 'addresses'), namespace='addresses')
    ),
    path(
        route='checkout/',
        view=include(('checkout.urls', 'checkout'), namespace='checkout')
    ),
    path(
        route='orders/',
        view=include(('orders.urls', 'orders'), namespace='orders')
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'
