from django.contrib import auth, messages
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from products.models import Basket
from users.forms import ProfileForm, UserLoginForm, UserRegisterForm
from users.models import EmailVerification, User


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

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class EmailVerificationView(TemplateView):
    template_name = 'users/email_succes_page.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)

        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return redirect('products:landing')

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
#     return render(request, 'users/login.html', context)

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
