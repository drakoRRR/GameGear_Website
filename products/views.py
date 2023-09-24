from django.shortcuts import render

from .models import ProductCategory, Product

# Create your views here.
def landing_page(request):
    context = {
        'categories': ProductCategory.objects.all(),
        'products': Product.objects.all()
    }

    return render(request, 'products/landing_page.html', context)


def products_page(request):
    context = {
        'categories': ProductCategory.objects.all(),
        'products': Product.objects.all()
    }

    return render(request, 'products/products_page.html', context)


def aboutus_page(request):
    return render(request, 'products/aboutus_page.html')


def contacts_page(request):
    return render(request, 'products/contacts_page.html')