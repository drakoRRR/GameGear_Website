from django.test import TestCase
from django.urls import reverse

from .models import ProductCategory, Product

from .views import search_paginate, PER_PAGE

from http import HTTPStatus

# Create your tests here.
class LandingViewTestCase(TestCase):
    fixtures = ('fixtures/categories.json', 'fixtures/products.json')

    def test_view(self):
        path = reverse('products:landing')
        response = self.client.get(path)
        categories = ProductCategory.objects.all()
        products = Product.objects.distinct('category')[:6]

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(list(response.context_data['categories']), list(categories))
        self.assertEquals(list(response.context_data['object_list']), list(products))
        self.assertTemplateUsed(response, 'products/landing_page.html')


class ProductsTestCase(TestCase):
    fixtures = ('fixtures/categories.json', 'fixtures/products.json')

    def setUp(self):
        self.page = 1
        self.category = ProductCategory.objects.first()
        self.products_all = Product.objects.all()

    def test_view_with_category(self):
        path = reverse('products:category', kwargs={'category_id': self.category.id})
        response = self.client.get(path)
        products = Product.objects.filter(category_id=self.category.id)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(list(response.context['products']), list(products))
        self.assertTemplateUsed(response, 'products/products_page.html')

    def test_pagination(self):
        path = reverse('products:paginator_without_category', kwargs={'page': self.page})
        response = self.client.get(path)

        page_paginate = search_paginate(products=self.products_all, sort_option=None, page=self.page)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(list(response.context['products']), list(page_paginate))
        self.assertEquals(response.context['current_sorting_option'], 'default')
        self.assertEqual(len(page_paginate), PER_PAGE)
        self.assertTemplateUsed(response, 'products/products.html')


class AboutUsViewTestCase(TestCase):
    def test_view(self):
        path = reverse('products:aboutus')
        response = self.client.get(path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/aboutus_page.html')


class ContactsViewTestCase(TestCase):
    def test_view(self):
        path = reverse('products:contacts')
        response = self.client.get(path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/contacts_page.html')






