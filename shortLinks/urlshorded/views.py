from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from urlshorded.models import *
from urlshorded.other import *
from .forms import GetUrlForm, RegisterUserForm, LoginUserForm
from django.views.generic import CreateView
from django.urls import reverse_lazy


def homepage(request):
    listcon = Links()
    ip_guest = get_client_ip(request)
    print(ip_guest)
    list_items = get_items_list(request)

    if request.method == 'POST':
        form = GetUrlForm(request.POST)
        if form.is_valid():
            add_new_url(request, form.cleaned_data['main_links'],)
            return redirect('home')
    else:
        form = GetUrlForm()

    param = {
        'list_items': list_items,
        'form': form,
    }
    return render(request, 'urlshorded/index.html', context=param)


def delete_link(request, id_link: int):
    link_con = Links()

    delete_url_info(request, id_link)
    return redirect('home')


def redirect_to_long_url(request, hash_url: str):
    link_con = Links()
    click_con = ClickToLinks()
    ip_guest = get_client_ip(request)

    if click_con.valid_guest(ip_guest, hash_url):
        click_con.add_new_click(ip_guest, hash_url)
    else:
        click_con.update_date_last_click(ip_guest, hash_url)

    return redirect(link_con.get_link_by_hash(hash_url))


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'urlshorded/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регестрація'
        return context


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'urlshorded/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизація'
        return context


def logout_user(request):
    logout(request)
    return redirect('home')
