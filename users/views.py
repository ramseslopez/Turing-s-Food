"""Users app views"""

from django.contrib import messages
from django.contrib.auth import views as auth_views, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

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
        send_email_confirmation(self.request)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    """User registry"""
    template_name = 'users/profile.html'


class ConfirmationSent(TemplateView):
    """Tells user that an email confirmation has been sent"""
    template_name = 'users/confirmation-sent.html'


class EmailConfirmation(LoginRequiredMixin, TemplateView):
    """Confirms an email"""
    template_name = 'users/email-confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'success' not in context:
            context['success'] = check_token(
                user=self.request.user,
                token=self.kwargs.get('token')
            )
        return context
