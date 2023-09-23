from django.shortcuts import render, redirect
from django.contrib import auth

from .models import User
from users.forms import UserLoginForm, UserRegisterForm

# Create your views here.
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect('products:landing')
    else:
        form = UserLoginForm()

    context = {
        'form': form
    }

    return render(request, 'users/login_page.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm()
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = UserRegisterForm()

    context = {
        'form': form
    }

    return render(request, 'users/register_page.html', context)