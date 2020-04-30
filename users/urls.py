"""Users app URL configuration"""

from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
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
]
