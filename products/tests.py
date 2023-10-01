from django.test import TestCase
from django.urls import reverse

from .models import ProductCategory, Product

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

    def test_data(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/products_page.html')