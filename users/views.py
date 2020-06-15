"""Users app views"""

from django.contrib import messages
from django.contrib.auth import views as auth_views, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, ListView, View
from django.shortcuts import redirect

from .forms import SignupForm
from .mixins import ReCaptchaV3Mixin
from .models import DeliveryMan
from .utils import send_email_confirmation, check_token


class LoginView(ReCaptchaV3Mixin, auth_views.LoginView):
    """Authenticates users"""
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        """Sets user's status to one"""
        user = form.get_user()
        user.status = 1
        user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class DeliveryMenLoginView(ReCaptchaV3Mixin, auth_views.LoginView):
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


class AdminLoginView(ReCaptchaV3Mixin, auth_views.LoginView):
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


class SignupView(ReCaptchaV3Mixin, FormView):
    """User registry"""
    form_class = SignupForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:confirmation_sent')

    # @check_recaptcha_v3
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


class DeliveryMenListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    """Lists all delivery men"""

    def test_func(self):
        """Checks if user is admin"""
        return self.request.user.status == 3

    model = DeliveryMan
    template_name = 'users/delivery-men.html'


class AddDeliveryManView(UserPassesTestMixin, LoginRequiredMixin, View):
    """Removes a delivery man"""

    def test_func(self):
        """Checks if user is admin"""
        return self.request.user.status == 3

    def post(self, request):
        """Removes item from menu"""
        data = {}
        email = request.POST.get('email')
        user_queryset = get_user_model().objects.filter(
            email=email
        )
        if not user_queryset.exists():
            data['message'] = 'El usuario no está registrado.'
            data['success'] = False
        else:
            user = user_queryset.get()
            if user.is_delivery_man:
                data['message'] = (
                    'El usuario ingresado ya ha sido registrado '
                    'como repartidor.'
                )
                data['success'] = False
            else:
                DeliveryMan.objects.create(user=user)
                user.is_delivery_man = True
                user.save()
                data['message'] = (
                    'Se ha registrado al usuario como repartidor.'
                )
                data['success'] = True
        return JsonResponse(data)


class RemoveDeliveryManView(UserPassesTestMixin, LoginRequiredMixin, View):
    """Removes a delivery man"""

    def test_func(self):
        """Checks if user is admin"""
        return self.request.user.status == 3

    def post(self, request):
        """Removes item from menu"""
        if request.user.status == 3:
            pk = int(request.POST.get('deleted_delivery_man'))
            delivery_man = DeliveryMan.objects.get(pk=pk)
            user = delivery_man.user
            user.is_delivery_man = False
            if user.status == 2:
                user.status = 1
            user.save()
            delivery_man.delete()
        return redirect('users:delivery_men')


class ActivatePickupView(UserPassesTestMixin, LoginRequiredMixin, View):
    """Sets delivery man as active"""

    def test_func(self):
        """Checks if user is delivery man"""
        return self.request.user.status == 2

    def get(self, request):
        """Sets delivery man as active"""
        delivery_man = request.user.deliveryman
        delivery_man.is_active = True
        delivery_man.is_available = True
        delivery_man.save()
        return redirect('orders:pickup_service')


class StopPickupView(UserPassesTestMixin, LoginRequiredMixin, View):
    """Sets delivery man as inactive"""

    def test_func(self):
        """Checks if user is delivery man"""
        return self.request.user.status == 2

    def get(self, request):
        """Sets delivery man as inactive"""
        delivery_man = request.user.deliveryman
        delivery_man.is_active = False
        delivery_man.is_available = False
        delivery_man.save()
        return redirect('orders:pickup_service')
