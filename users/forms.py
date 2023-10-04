import uuid
from datetime import timedelta

from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.utils.timezone import now

from users.models import EmailVerification, User

from .tasks import send_email_verification

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    username = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.EmailInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=True)
        send_email_verification.delay(user.id)
        return user


class ProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4'
    }))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input',
    }), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'readonly': True
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'readonly': True
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email')