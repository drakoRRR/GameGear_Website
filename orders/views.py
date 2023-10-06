from http import HTTPStatus

import stripe
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from gamegearsite import settings
from orders.forms import OrderForm
from orders.models import Order
from products.models import Basket

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
class SuccessView(TemplateView):
    template_name = 'orders/order_success_page.html'


class CanceledView(TemplateView):
    template_name = 'orders/canceled.html'


class OrderListView(ListView):
    template_name = 'orders/orders_page.html'
    queryset = Order.objects.all()
    ordering = ('-created')

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order_item_page.html'
    model = Order


class OrderCreateView(CreateView):
    template_name = 'orders/order_page.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:create_order')

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)

        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:success_order')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:canceled_order')),
            metadata={
                'order_id': self.object.id,
            }
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)

@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        line_items = session.line_items
        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = session.metadata['order_id']
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
