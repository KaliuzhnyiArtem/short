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


#
def generate_url_hash() -> str:

    link_con = Links()
    while True:
        url_hash = ''.join(choice(string.ascii_letters + string.digits+'-') for _ in range(6))
        if link_con.valid_hash(url_hash):
            return url_hash


