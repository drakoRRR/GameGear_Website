from django.shortcuts import render
from django.views.generic import CreateView


# Create your views here.
class OrderCreateView(CreateView):
    template_name = 'orders/order_page.html'
