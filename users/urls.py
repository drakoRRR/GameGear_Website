from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signin/', views.login, name='login'),
    path('signup/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
