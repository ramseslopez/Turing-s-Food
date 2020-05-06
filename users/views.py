"""Users app views"""

from django.contrib import messages
from django.contrib.auth import views as auth_views, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.shortcuts import redirect

from .forms import SignupForm
from .utils import send_email_confirmation, check_token


class LoginView(auth_views.LoginView):
    """Authenticates users"""
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        """Sets user's status to one"""
        user = form.get_user()
        user.status = 1
        user.save()
        return super().form_valid(form)


class DeliveryMenLoginView(auth_views.LoginView):
    """Authenticates delivery men"""
    template_name = 'users/delivery-men-login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        """
        Checks if users have the correct permissions,
        and changes their status.
        """
        user = form.get_user()
        if not user.is_delivery_man:
            form.add_error(
                field='__all__',
                error=(
                    'No puedes entrar como repartidor. '
                    'Un administrador debe darte de alta como repartidor'
                )
            )
            return super().form_invalid(form)
        user.status = 2
        user.save()
        return super().form_valid(form)


class AdminLoginView(auth_views.LoginView):
    """Authenticates admins"""
    template_name = 'users/admin-login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        """
        Checks if users have the correct permissions,
        and changes their status.
        """
        user = form.get_user()
        if not user.is_admin:
            form.add_error(
                field='__all__',
                error=(
                    'No puedes entrar como repartidor. '
                    'Un administrador debe darte de alta como repartidor'
                )
            )
            return super().form_invalid(form)
        user.status = 3
        user.save()
        return super().form_valid(form)


class SignupView(FormView):
    """User registry"""
    form_class = SignupForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:confirmation_sent')

    def form_valid(self, form):
        """Saves user"""
        user = form.save()
        messages.success(
            request=self.request,
            message=(
                'Parry ha enviado tu código de confirmacion a: ' +
                f'{user.email}, ¡No lo hagas esperar!'
            )
        )
        send_email_confirmation(user, self.request)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    """User registry"""
    template_name = 'users/profile.html'


class ConfirmationSent(TemplateView):
    """Tells user that an email confirmation has been sent"""
    template_name = 'users/confirmation-sent.html'


class ActivateAccount(TemplateView):
    """Activates an account"""
    template_name = 'users/activation-failed.html'

    def get(self, request, *args, **kwargs):
        """Checks token and activates it"""
        user = get_user_model().objects.get(pk=self.kwargs.get('pk'))
        valid_token = check_token(
            user=user,
            token=self.kwargs.get('token')
        )

        if valid_token:
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:profile')

        return super().get(request, *args, **kwargs)
