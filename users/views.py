from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView

from users.forms import UserLoginForm, UserRegisterForm, ProfileForm
from products.models import Basket
from users.models import User


# Create your views here.
class LoginUserView(LoginView):
    template_name = 'users/login_page.html'
    form_class = UserLoginForm

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error with username or password, check again !')
        return super().form_invalid(form)


class RegistrationView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register_page.html'
    success_url = reverse_lazy('products:landing')

    def form_valid(self, form):
        response = super().form_valid(form)
        auth.login(self.request, self.object)
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error with username or password, check again !')
        return super().form_invalid(form)


class ProfileView(UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'users/profile_page.html'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data()
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = ProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('users:profile')
#     else:
#         form = ProfileForm(instance=request.user)
#
#     context = {
#         'form': form,
#         'baskets': Basket.objects.filter(user=request.user),
#     }
#
#     return render(request, 'users/profile_page.html', context)

# def logout(request):
#     auth.logout(request)
#     return redirect('products:landing')

# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request.POST)
#
#         # if form.is_valid():  # in prod, check the values
#
#         username = request.POST['username']
#         password = request.POST['password']
#         user = auth.authenticate(username=username, password=password)
#         if user:
#             auth.login(request, user)
#             return redirect('products:landing')
#         else:
#             messages.success(request, 'There was an error with username or password, check again !')
#             return redirect('users:login')
#     else:
#         form = UserLoginForm()
#
#     context = {
#         'form': form
#     }
#
#     return render(request, 'users/login_page.html', context)

# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user = auth.authenticate(username=username, password=password)
#             auth.login(request, user)
#             return redirect('products:landing')
#         else:
#             messages.success(request, 'There was an error with username or password, check again !')
#             return redirect('users:register')
#     else:
#         form = UserRegisterForm()
#
#     context = {
#         'form': form
#     }
#
#     return render(request, 'users/register_page.html', context)