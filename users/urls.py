from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'users'

urlpatterns = [
    path('signin/', views.LoginUserView.as_view(), name='login'),
    path('signup/', views.RegistrationView.as_view(), name='register'),

    path('profile/<int:pk>/', login_required(views.ProfileView.as_view()), name='profile'),

    path('logout/', LogoutView.as_view(), name='logout'),

    path('verify/<str:email>/<uuid:code>/', views.EmailVerificationView.as_view(), name='email_verification'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset_page.html'),
         name='reset_password'),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/reset_password_sent_page.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_form.html'),
         name='password_reset_confirm'),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_complete'),
]
