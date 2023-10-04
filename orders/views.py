import stripe

from http import HTTPStatus

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView

from gamegearsite import settings
from orders.forms import OrderForm


stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
class SuccessView(TemplateView):
    template_name = 'orders/order_success_page.html'


class CanceledView(TemplateView):
    template_name = 'orders/canceled.html'


class OrderCreateView(CreateView):
    template_name = 'orders/order_page.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:create_order')

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1NxcJpLhQJgpKyIBqxBCl8ib',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:success_order')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:canceled_order')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)
