from django.urls import path, include
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('products/', views.products_page, name='products'),
    path('shoppinglist/', views.shoppinglist_page, name='shoppinglist'),
    path('aboutus/', views.aboutus_page, name='aboutus'),
    path('contacts/', views.contacts_page, name='contacts'),
]
