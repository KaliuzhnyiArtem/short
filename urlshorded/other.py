from random import choice
import string

from urlshorded.forms import GetUrlForm
from urlshorded.models import *


def get_client_ip(request) -> str:
    """Повертає IP користувача"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def generate_url_hash() -> str:
    """Генерує та повертає url_hash"""
    link_con = Links()
    while True:
        url_hash = ''.join(choice(string.ascii_letters + string.digits+'-') for _ in range(6))
        if link_con.valid_hash(url_hash):
            return url_hash


def get_items_list(request):
    """Повертає список з інформацією про всі URL користувача"""
    listcon = Links()
    guestcon = Guests()
    guest_ip = get_client_ip(request)

    if request.user.is_authenticated:
        return listcon.get_user_data(request.user.id)
    else:
        if guestcon.find_guest(guest_ip):
            return listcon.get_guest_data(guest_ip)
        else:
            guestcon.add_new_guest(guest_ip)


def add_new_url(request, link: str):
    """Перевіряє хто створює short link гість чи юзер.
    Додає данні в таблицю про довгу і коротку URL """
    listcon = Links()
    hash_url = generate_url_hash()
    guest = Guests()

    if request.user.is_authenticated:
        listcon.add_new_link_user(link, hash_url, request.user.id)
    else:
        listcon.add_new_link_guest(link, hash_url,
                                   guest.get_id_guests(get_client_ip(request)))


def delete_url_info(request, link_id: int):
    """Видаляє URl не фізично, ставить флаг про видалення.
    Робить 2 перевірки чи авторизований, та чи має доступ до видалення"""
    linkcon = Links()

    if request.user.is_authenticated:
        if _validation_access_user(request.user.id, link_id):
            linkcon.delete_link(link_id)
    else:
        if _validation_access_guest(request, link_id):
            linkcon.delete_link(link_id)


def _validation_access_user(user_id: int, link_id: int) -> bool:
    """Перевіряє чи є User власником URL"""
    linkcon = Links()
    if user_id == linkcon.get_id_owner_link_for_user(link_id):
        return True
    else:
        return False


def _validation_access_guest(request, link_id: int) -> bool:
    """Перевіряє чи є Guest власником URL"""
    linkcon = Links()
    guest = Guests()

    if guest.get_id_guests(get_client_ip(request)) == linkcon.get_ip_owner_link_for_guest(link_id):
        return True
    else:
        return False


def handler_post_request_in_url_form(request):
    """Обробляє POST запрос отриманий через форму.
    При успішній валідації додає  URL в базу"""
    if request.method == 'POST':
        form = GetUrlForm(request.POST)
        if form.is_valid():
            add_new_url(request, form.cleaned_data['main_links'],)
            return True


def get_context_for_homepage(request) -> dict:
    """Повертає контекст для Головної сторінки"""
    return {
        'list_items': get_items_list(request),
        'form': GetUrlForm(),
    }


def add_new_click(request, hash_url: str) -> None:
    """Перевіряємо чи унікальний перехід.
    Додаємо новий перхід в таблицю або
    оновлюємо дату останнього переходу"""

    click_con = ClickToLinks()
    link_con = Links()
    id_link = link_con.get_idlink_by_hash(hash_url)
    ip_guest = get_client_ip(request)

    if _valid_guest(ip_guest, hash_url):
        click_con.add_new_click(ip_guest, id_link)
    else:
        click_con.update_date_last_click(ip_guest, id_link)


def _valid_guest(ip_guest: str, hash_url) -> bool:
    """Перевіряє чи раніше переходив гість по короткому URL"""
    click_con = ClickToLinks()
    link_con = Links()
    id_link = link_con.get_idlink_by_hash(hash_url)

    if click_con.get_guest_by_ip_and_id_link(ip_guest, id_link):
        return False
    else:
        return True


def get_link_by_hash(hash_url):
    """Повертає Url за переданим hash_url """
    link_con = Links()
    return link_con.get_link_by_hash(hash_url)


def create_short_url_use_api(request) -> str:
    """Додає новий запис з довгим та коротким URL в таблицю
    Повертає коротке URL"""
    linc_con = Links()
    hash_url = generate_url_hash()
    linc_con.create_short_url_use_api(request, hash_url)

    return '127.0.0.1:8000/redirect/' + hash_url


def plus_do(a, b):
    return a+b

