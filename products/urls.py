from django.urls import path, include
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('goods/', views.products_page, name='products'),
    path('goods/page/<int:page_number>/', views.products_page, name='paginator_without_category'),
    path('catalog/<int:category_id>/', views.products_page, name='category'),
    path('catalog/<int:category_id>/page/<int:page_number>/', views.products_page, name='paginator'),
    path('aboutus/', views.aboutus_page, name='aboutus'),
    path('contacts/', views.contacts_page, name='contacts'),
    path('baskets/add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', views.basket_remove, name='basket_remove'),
]
