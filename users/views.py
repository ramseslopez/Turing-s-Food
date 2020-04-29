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
    redirect_authenticated_user = False


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


class MenuView(TemplateView):
    """ Menu View """

    template_name = 'restaurant/menu.html'


class IndexView(TemplateView):
    """ Index View """

    template_name = 'index.html'


class OrdersView(TemplateView):
    """ Orders View """

    template_name = 'orders/orders.html'


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
