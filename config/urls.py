"""turing_food URL Configuration"""

from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view=RedirectView.as_view(url=reverse_lazy('users:login')), name='index'),
    path('users/', include(('users.urls', 'users'), namespace='users')),
]
