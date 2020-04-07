"""Users app views"""

from django.contrib.auth import views as auth_views, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.shortcuts import render

from .forms import SignupForm


class LoginView(auth_views.LoginView):
    """Authenticates users"""
    template_name = 'users/login.html'
    redirect_authenticated_user = False


class SignupView(FormView):
    """User registry"""
    form_class = SignupForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        """Saves user"""
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    """User registry"""
    template_name = 'users/profile.html'

class MenuView(TemplateView):
    """ Menu View """

    template_name = 'menu.html'

    def get(self, request):
        return render(request, self.template_name)



