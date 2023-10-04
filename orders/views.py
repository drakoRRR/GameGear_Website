from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from orders.forms import OrderForm


# Create your views here.
class OrderCreateView(CreateView):
    template_name = 'orders/order_page.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:create_order')

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)
