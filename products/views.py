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


# class ProductsView(ListView):
#     model = Product
#     template_name = 'products/products_page.html'
#     paginate_by = 6
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         category_id = self.kwargs.get('category_id')
#         search_query = self.request.GET.get('search')
#         sort_option = self.request.GET.get('sorting-products')
#
#         if category_id:
#             queryset = queryset.filter(category_id=category_id)
#         if search_query:
#             queryset = queryset.filter(name__icontains=search_query)
#
#         sorting_options = {
#             'alphabet': 'name',
#             'low-high': 'price',
#             'high-low': '-price'
#         }
#
#         if sort_option in sorting_options:
#             sort_field = sorting_options[sort_option]
#             queryset = queryset.order_by(sort_field)
#
#         return queryset
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data()
#         context['categories'] = ProductCategory.objects.all()
#         context['category_id'] = self.kwargs.get('category_id')
#         context['search_query'] = self.request.GET.get('search')
#         context['sort_option'] = self.request.GET.get('sorting-products')
#         return context
#
#     def get_paginate_by(self, queryset):
#         if self.request.GET.get('search') is not None or self.request.GET.get('sorting-products') is not None:
#             return None
#         return super().get_paginate_by(queryset)


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


def product_list(request, category_id=None, page=1):
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    sort_option = request.GET.get('sorting-products')

    sorting_options = {
        'alphabet': 'name',
        'low-high': 'price',
        'high-low': '-price',
    }

    sort_field = sorting_options.get(sort_option)
    if sort_field:
        products = products.order_by(sort_field)

    per_page = 6
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page)

    context = {
        'categories': ProductCategory.objects.all(),
        'products': products_paginator,
        'category_id': category_id,
        'current_sorting_option': request.GET.get('sorting-products', 'default'),
    }

    return render(request, 'products/products_page.html', context)

def sort(request, category_id=None, page=1):
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    sort_option = request.GET.get('sorting-products')
    search_query = request.GET.get('search', '')

    if search_query:
        products = products.filter(name__icontains=search_query)

    sorting_options = {
        'alphabet': 'name',
        'low-high': 'price',
        'high-low': '-price',
    }

    sort_field = sorting_options.get(sort_option)
    if sort_field:
        products = products.order_by(sort_field)

    per_page = 6
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page)

    context = {
        'categories': ProductCategory.objects.all(),
        'products': products_paginator,
        'category_id': category_id,
        'page': page,
        'search_query': search_query,
        'current_sorting_option': request.GET.get('sorting-products', 'default'),
    }

    return render(request, 'products/products_page.html', context)


def search(request, page=1):
    search_query = request.GET.get('search')
    sort_option = request.GET.get('sorting-products')

    if search_query is None:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(name__icontains=search_query)

    sorting_options = {
        'alphabet': 'name',
        'low-high': 'price',
        'high-low': '-price',
    }

    sort_field = sorting_options.get(sort_option)
    if sort_field:
        products = products.order_by(sort_field)

    per_page = 6
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page)

    context = {
        'categories': ProductCategory.objects.all(),
        'products': products_paginator,
        'search_query': search_query,
        'current_sorting_option': sort_option,
        'flag_search': True
    }

    return render(request, 'products/products_page.html', context)


