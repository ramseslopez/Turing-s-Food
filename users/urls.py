"""Users app URL configuration"""

from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path(
        route='login/delivery-man',
        view=views.DeliveryMenLoginView.as_view(),
        name='delivery_men_login'
    ),
    path(
        route='login/admin',
        view=views.AdminLoginView.as_view(),
        name='admin_login'
    ),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path(
        route='confirmation-sent/',
        view=views.ConfirmationSent.as_view(),
        name='confirmation_sent'
    ),
    path(
        route='activate-account/<int:pk>/<str:token>/',
        view=views.ActivateAccount.as_view(),
        name='activate_account'
    ),
    path(
        route='delivery-men/',
        view=views.DeliveryMenListView.as_view(),
        name='delivery_men'
    ),
    path(
        route='delivery-men/add',
        view=views.AddDeliveryManView.as_view(),
        name='add_delivery_man'
    ),
    path(
        route='delivery-men/remove',
        view=views.RemoveDeliveryManView.as_view(),
        name='remove_delivery_man'
    ),
]
