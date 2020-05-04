"""Restaurants URL config"""

from django.urls import path

from . import views


urlpatterns = [
    path('', views.RestaurantListView.as_view(), name='index'),
    path('register', views.RestaurantFormView.as_view(), name='register'),
    path(
        route='restaurant/<slug:slug>',
        view=views.RestaurantDetailView.as_view(),
        name='detail'
    ),
]
