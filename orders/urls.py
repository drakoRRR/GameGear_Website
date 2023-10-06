from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('order-create/', views.OrderCreateView.as_view(), name='create_order'),
    path('order-success/', views.SuccessView.as_view(), name='success_order'),
    path('order-canceled/', views.CanceledView.as_view(), name='canceled_order'),
    path('', views.OrderListView.as_view(), name='orders')
]
