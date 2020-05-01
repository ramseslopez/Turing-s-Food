"""Users app URL configuration"""

from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf.urls import handler404
from django.conf.urls import handler500
from users.views import error_404
from users.views import error_500

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

handler404 = error_404
handler500 = error_500
