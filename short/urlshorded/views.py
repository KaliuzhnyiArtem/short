from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .forms import RegisterUserForm, LoginUserForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from urlshorded.other import handler_post_request_in_url_form, \
    get_context_for_homepage, delete_url_info, generate_url_hash,\
    add_new_click, get_link_by_hash


def homepage(request):
    """Головна сторінка"""
    if handler_post_request_in_url_form(request) is not None:
        return redirect('home')

    return render(request=request,
                  template_name='urlshorded/index.html',
                  context=get_context_for_homepage(request))


def delete_link(request, id_link: int):
    """При натисканні на кнопку, видаляє нефізично данні про URL з бази"""
    delete_url_info(request, id_link)
    return redirect('home')


def redirect_to_long_url(request, hash_url: str):
    """Робить редірект з скороченого посилання на довге"""
    add_new_click(request, hash_url)
    return redirect(get_link_by_hash(hash_url))


class RegisterUser(CreateView):
    """Регестрація нового користувача"""
    form_class = RegisterUserForm
    template_name = 'urlshorded/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регестрація'
        return context


class LoginUser(LoginView):
    """Сторінка для авторизації користувача"""
    form_class = LoginUserForm
    template_name = 'urlshorded/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизація'
        return context


def logout_user(request):
    """Робить виходить з акаунту"""
    logout(request)
    return redirect('home')


# API
class SHORTURL(APIView):
    def post(self, request):
        hash_url = generate_url_hash()
        Links.objects.create(main_links=request.data['link'], short_links=hash_url)

        short_url = '127.0.0.1:8000/redirect/'+hash_url
        return Response({'short_link': short_url})
