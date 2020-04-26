"""Users app views"""

from django.contrib.auth import views as auth_views, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.core.mail import send_mail
from django.conf import settings

from .forms import SignupForm


class LoginView(auth_views.LoginView):
    """Authenticates users"""
    template_name = 'users/login.html'
    redirect_authenticated_user = False


class SignupView(FormView):
    """User registry"""
    form_class = SignupForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:confirmation_send')

    def form_valid(self, form):
        """Saves user"""
        user = form.save()
        login(self.request, user)
        subject = '¡Gracias por registrarte en Turings Food!'
        message = 'Tu código de confirmacion es 12345'
        email_from = settings.env(EMAIL_HOST_USER)
        recipient_list = ['repv1999@ciencias.unam.mx',]
        send_mail( subject, message, email_from, recipient_list )
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    """User registry"""
    template_name = 'users/profile.html'

class EmailConfirmation(LoginRequiredMixin, TemplateView):
    """Confirmation Code Send"""
    template_name = 'users/confirmation_send.html'
