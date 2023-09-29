from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('goods/', views.product_list, name='products'),
    path('goods/page/<int:page>/', views.product_list, name='paginator_without_category'),
    path('catalog/<int:category_id>/', views.product_list, name='category'),
    path('catalog/<int:category_id>/page/<int:page>/', views.product_list, name='paginator'),
    path('aboutus/', views.AboutUsView.as_view(), name='aboutus'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('baskets/add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', views.basket_remove, name='basket_remove'),
    path('goods/search/<int:page>/', views.search, name='search_view'),
    path('goods/<int:category_id>/sort/<int:page>/', views.sort, name='sort'),
    path('goods/sort/<int:page>/', views.sort, name='sort_no_category'),
    path('goods/product/<int:product_id>', views.product_page, name='product')
]
