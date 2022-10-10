from random import choice
import string
from urlshorded.models import *


def get_client_ip(request) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def generate_url_hash() -> str:
    link_con = Links()
    while True:
        url_hash = ''.join(choice(string.ascii_letters + string.digits+'-') for _ in range(6))
        if link_con.valid_hash(url_hash):
            return url_hash


def get_items_list(request):
    listcon = Links()

    if request.user.is_authenticated:
        return listcon.get_user_data(request.user.id)
    else:
        return listcon.get_guest_data(get_client_ip(request))


def add_new_url(request, link: str):
    listcon = Links()
    hash = generate_url_hash()

    if request.user.is_authenticated:
        listcon.add_new_link_user(link, hash, request.user.id)
    else:
        listcon.add_new_link_guest(link, hash, get_client_ip(request))


def delete_url_info(request, link_id: int):
    linkcon = Links()

    if request.user.is_authenticated:
        if linkcon.validation_access_user(request.user.id, link_id):
            linkcon.delete_link(link_id)
    else:
        if linkcon.validation_access_guest(link_id, get_client_ip(request)):
            linkcon.delete_link(link_id)

