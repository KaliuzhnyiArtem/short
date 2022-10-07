from django.shortcuts import render, redirect
from django.http import HttpResponse
from urlshorded.models import *
from urlshorded.other import get_client_ip, generate_url_hash
from .forms import GetUrlForm


def testpage(request):
    listcont = Links()
    ip_guest = get_client_ip(request)

    if request.method == 'POST':
        form = GetUrlForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = GetUrlForm()

    param = {
        'list_items': listcont.get_guest_data(ip_guest),
        'hash': generate_url_hash(),
        'form': form
    }
    return render(request, 'urlshorded/index.html', context=param)

