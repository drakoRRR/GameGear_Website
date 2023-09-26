from django.urls import path, include
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('goods/', views.ProductsView.as_view(), name='products'),
    path('goods/page/<int:page>/', views.ProductsView.as_view(), name='paginator_without_category'),
    path('catalog/<int:category_id>/', views.ProductsView.as_view(), name='category'),
    path('catalog/<int:category_id>/page/<int:page>/', views.ProductsView.as_view(), name='paginator'),
    path('aboutus/', views.AboutUsView.as_view(), name='aboutus'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('baskets/add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', views.basket_remove, name='basket_remove'),
    path('goods/search/', views.ProductsView.as_view(), name='search_view'),
]
