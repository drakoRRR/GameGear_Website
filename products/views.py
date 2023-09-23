from django.shortcuts import render

# Create your views here.
def landing_page(request):
    return render(request, 'products/landing_page.html')


def products_page(request):
    return render(request, 'products/products_page.html')


def aboutus_page(request):
    return render(request, 'products/aboutus_page.html')


def shoppinglist_page(request):
    return render(request, 'products/shoppinglist_page.html')


def contacts_page(request):
    return render(request, 'products/contacts_page.html')