from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from .models import ProductCategory, Product, Basket

# Create your views here.
class LandingView(ListView):
    model = Product
    template_name = 'products/landing_page.html'

    def get_queryset(self):
        queryset = super(LandingView, self).get_queryset()
        return queryset.distinct('category')[:6]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LandingView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context


class ProductsView(ListView):
    model = Product
    template_name = 'products/products_page.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = super(ProductsView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        context['category_id'] = self.kwargs.get('category_id')
        return context


class AboutUsView(TemplateView):
    template_name = 'products/aboutus_page.html'


class ContactsView(TemplateView):
    template_name = 'products/contacts_page.html'


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.filter(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])