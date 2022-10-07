from django.shortcuts import render, redirect
from django.http import HttpResponse
from urlshorded.models import *
from urlshorded.other import get_client_ip, generate_url_hash


def testpage(request):
    listcont = Links()
    ip_guest = get_client_ip(request)

    param = {
        'list_items': listcont.get_guest_data(ip_guest),
        'hash': generate_url_hash()
    }
    return render(request, 'urlshorded/index.html', context=param)

