"""Users app URL configuration"""

from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='indexx'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('menu/', views.MenuView.as_view(), name = 'menu'),
    path('orders/', views.OrdersView.as_view(), name = 'orders'),
]