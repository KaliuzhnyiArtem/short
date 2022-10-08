from django.shortcuts import render, redirect
from urlshorded.models import *
from urlshorded.other import get_client_ip, generate_url_hash
from .forms import GetUrlForm
from django.http import HttpResponse


def homepage(request):
    listcon = Links()
    ip_guest = get_client_ip(request)

    if request.method == 'POST':
        form = GetUrlForm(request.POST)
        if form.is_valid():
            hash = generate_url_hash()
            listcon.add_new_link(form.cleaned_data['main_links'],
                                 hash=hash,
                                 owner_ip=ip_guest,
                                 )
            return redirect('home')
    else:
        form = GetUrlForm()

    param = {
        'list_items': listcon.get_guest_data(ip_guest),
        'form': form
    }
    return render(request, 'urlshorded/index.html', context=param)


def delete_link(request, id_link):
    link_con = Links()

    if link_con.validation_access_guest(id_link, get_client_ip(request)):
        link_con.delete_link(id_link)
    return redirect('home')


#
# def redirect_to_long_url():
#     return redirect()