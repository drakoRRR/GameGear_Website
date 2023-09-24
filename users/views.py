from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from users.forms import UserLoginForm, UserRegisterForm, ProfileForm
from products.models import Basket

# Create your views here.
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        # if form.is_valid():  # in prod, check the values

        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('products:landing')
        else:
            messages.success(request, 'There was an error with username or password, check again !')
            return redirect('users:login')
    else:
        form = UserLoginForm()

    context = {
        'form': form
    }

    return render(request, 'users/login_page.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect('products:landing')
        else:
            messages.success(request, 'There was an error with username or password, check again !')
            return redirect('users:register')
    else:
        form = UserRegisterForm()

    context = {
        'form': form
    }

    return render(request, 'users/register_page.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=request.user)

    context = {
        'form': form,
        'baskets': Basket.objects.filter(user=request.user),
    }

    return render(request, 'users/profile_page.html', context)

def logout(request):
    auth.logout(request)
    return redirect('products:landing')