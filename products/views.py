from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import ProductCategory, Product, Basket

# Create your views here.
def landing_page(request):
    context = {
        'categories': ProductCategory.objects.all(),
        'products': Product.objects.distinct('category')[:6]
    }

    return render(request, 'products/landing_page.html', context)


def products_page(request, category_id=None, page_number=1):
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()

    per_page = 6
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page_number)

    context = {
        'categories': ProductCategory.objects.all(),
        'products': products_paginator,
        'category_id': category_id
    }

    return render(request, 'products/products_page.html', context)


def aboutus_page(request):
    return render(request, 'products/aboutus_page.html')


def contacts_page(request):
    return render(request, 'products/contacts_page.html')

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