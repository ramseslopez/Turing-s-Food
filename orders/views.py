"""Orders app views"""

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, View

from .models import Order
from .utils import ask_for_rating


class OrderListView(LoginRequiredMixin, ListView):
    """Shows user orders"""
    model = Order
    template_name = 'orders/list.html'

    def get_queryset(self):
        """Filters queryset by requesting user"""
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class OrderAttendView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    """Attending orders view"""
    model = Order
    template_name = 'orders/attend.html'

    def test_func(self):
        """Checks if user is admin"""
        return self.request.user.status == 3

    def get_queryset(self):
        """Filters queryset by status 1 or 2"""
        queryset = super().get_queryset()
        return queryset.filter(status__in=[1, 2])


class OrderPickUpServiceView(
    UserPassesTestMixin, LoginRequiredMixin, ListView
):
    """Pickup orders views"""
    model = Order
    template_name = 'orders/pickup.html'

    def test_func(self):
        """Checks if user is delivery man"""
        return self.request.user.status == 2

    def get_queryset(self):
        """Filters queryset by status 3"""
        queryset = super().get_queryset()
        return queryset.filter(status=3)

    def get_context_data(self, **kwargs):
        """Adds Google Cloud API Key to context"""
        context = super().get_context_data(**kwargs)
        if 'GOOGLE_CLOUD_API_KEY' not in context:
            context['GOOGLE_CLOUD_API_KEY'] = settings.GOOGLE_CLOUD_API_KEY
        return context


class OrderTakenView(UserPassesTestMixin, LoginRequiredMixin, View):
    """Marks as taken a order"""

    def test_func(self):
        """Checks if user is delivery man"""
        return self.request.user.status == 3

    def post(self, request):
        """Marks as taken a given order"""
        pk = int(request.POST.get('order'))
        order = Order.objects.get(pk=pk)
        order.status = 2
        order.save()
        return redirect('orders:attend')


class OrderPreparedView(UserPassesTestMixin, LoginRequiredMixin, View):
    """Marks as prepared a order"""

    def test_func(self):
        """Checks if user is delivery man"""
        return self.request.user.status == 3

    def post(self, request):
        """Marks as prepared a given order"""
        pk = int(request.POST.get('order'))
        order = Order.objects.get(pk=pk)
        order.status = 3
        order.save()
        return redirect('orders:attend')


class OrderDeliveredView(UserPassesTestMixin, LoginRequiredMixin, View):
    """Marks a order as delivered"""

    def test_func(self):
        """Checks if user is delivery man"""
        return self.request.user.status == 2

    def get(self, request):
        """Sets order as delivered"""
        delivery_man = request.user.deliveryman
        order = delivery_man.current_delivery
        delivery_man.is_available = True
        delivery_man.current_delivery = None
        order.status = 5
        delivery_man.save()
        order.save()
        ask_for_rating(order, request)
        return redirect('orders:pickup_service')


class OrderPickUpView(UserPassesTestMixin, LoginRequiredMixin, View):
    """Assigns orders to delivery men"""

    def test_func(self):
        """Checks if user is delivery man"""
        return self.request.user.status == 2

    def get(self, request):
        """If available, assigns orders to delivery men"""
        data = {}
        orders = Order.objects.filter(status=3)

        if orders.exists():
            order = orders.order_by('-ordered_at').first()
            user = self.request.user
            delivery_man = user.deliveryman

            order.status = 4
            order.delivery_man = user
            delivery_man.current_delivery = order
            delivery_man.is_available = False
            order.save()
            delivery_man.save()
            data['success'] = True
            data['message'] = 'Órden asignada correctamente'
        else:
            data['success'] = False
            data['message'] = 'No hay órdenes por recoger'

        return JsonResponse(data)


class OrderRateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    """Asks user for rate a order"""
    model = Order
    template_name = 'orders/rate.html'
    fields = ['rating', ]
    success_url = reverse_lazy('menu:items')

    def test_func(self):
        """Checks if user owns this order and is not rated yet"""
        order_pk = self.kwargs.get('pk')
        order = get_object_or_404(Order, pk=order_pk, rating=None)
        return self.request.user == order.user
