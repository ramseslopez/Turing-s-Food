"""Orders app URL config"""

from django.urls import path

from . import views


urlpatterns = [
    path('', views.OrderListView.as_view(), name='list'),
    path('attend', views.OrderAttendView.as_view(), name='attend'),
    path(
        route='pickup-service',
        view=views.OrderPickUpServiceView.as_view(),
        name='pickup_service'
    ),
    path('taken', views.OrderTakenView.as_view(), name='taken'),
    path('prepared', views.OrderPreparedView.as_view(), name='prepared'),
    path('pickup', views.OrderPickUpView.as_view(), name='pickup'),
    path('delivered', views.OrderDeliveredView.as_view(), name='delivered'),
    path('rate/<int:pk>', views.OrderRateView.as_view(), name='rate'),
]
