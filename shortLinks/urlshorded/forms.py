from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import *


class GetUrlForm(forms.Form):
    main_links = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form_for_ulr',
                                                                         'placeholder': "www.google.com",
                                                                         }))


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'regform',
                                                                            }))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'regform',
                                                                                  }))
    password2 = forms.CharField(label='Повторіть пароль', widget=forms.PasswordInput(attrs={'class': 'regform',
                                                                                            }))
    # class Meta:
    #     model = User
    #     fields = ('username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'logform',
                                                                            }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'logform',
                                                                                  }))


