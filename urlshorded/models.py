from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from datetime import datetime
from django.conf import settings


class Guests(models.Model):
    ip = models.TextField()

    def get_id_guests(self, ip_guest: str):
        """Повертає id гостя по його ip"""
        id_guest = Guests.objects.filter(ip=ip_guest)
        if id_guest:
            return id_guest[0].pk

    def add_new_guest(self, guest_ip):
        """Створює ного гостя в базі"""
        Guests.objects.create(ip=guest_ip)

    def find_guest(self, guest_ip: str):
        """Перевіряє чи є такий гість в базі"""
        if Guests.objects.filter(ip=guest_ip):
            return True
        else:
            return False


class Links(models.Model):
    main_links = models.TextField(blank=False)
    short_links = models.TextField(blank=False)
    deleted = models.BooleanField(default=False)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    owner_ip = models.ForeignKey('Guests', on_delete=models.CASCADE, null=True)

    def get_guest_data(self, ip='127.0.0.1'):
        """Повертає список данних про всі URL гостя"""
        guest = Guests()
        id_guest = guest.get_id_guests(ip)
        list_items = Links.objects.raw(
            f'SELECT *, (SELECT  count(id_links_id) FROM  urlshorded_clicktolinks WHERE id_links_id=urlshorded_links.id GROUP BY (id_links_id))  as cliks, (SELECT time_visit FROM urlshorded_clicktolinks WHERE id_links_id=urlshorded_links.id ORDER BY time_visit DESC LIMIT 1) as time_visit  FROM urlshorded_links WHERE (owner_ip_id={id_guest} AND  deleted=False) ORDER BY id DESC'
        )
        return list_items

    def get_user_data(self, id_user: int):
        """Повертає список данних про всі URL юзера"""
        list_items = Links.objects.raw(
            f'SELECT *, (SELECT  count(id_links_id) FROM  urlshorded_clicktolinks WHERE id_links_id=urlshorded_links.id GROUP BY (id_links_id))  as cliks, (SELECT time_visit FROM urlshorded_clicktolinks WHERE id_links_id=urlshorded_links.id ORDER BY time_visit DESC LIMIT 1) as time_visit  FROM urlshorded_links WHERE (owner_id_id={id_user} AND  deleted=False) ORDER BY id DESC'
        )
        return list_items

    def valid_hash(self, url_hash: str) -> bool:
        """Перевіряє чи є переданий url_hash в базі"""
        if Links.objects.filter(short_links=url_hash):
            return False
        else:
            return True

    def add_new_link_guest(self, link: str, hash_url: str, id_guest: int) -> None:
        """Додає новий запис від Гостя з long url, short url, user_id"""
        Links.objects.create(main_links=link, short_links=hash_url, owner_ip_id=id_guest)

    def add_new_link_user(self, link: str, hash_url, user_id: str):
        """Додає новий запис від Юзера з long url, short url, user_id"""
        Links.objects.create(main_links=link, short_links=hash_url, owner_id_id=user_id)

    def delete_link(self, id_link: int) -> None:
        """Установлює влаг видалення на True"""
        Links.objects.filter(pk=id_link).update(deleted=True)

    def get_ip_owner_link_for_guest(self, id_link: int,) -> str:
        """Повертає ip власника URL по id_link
        (для неавторизованих користувачів)"""
        return Links.objects.values('owner_ip_id').filter(pk=id_link)[0]['owner_ip_id']

    def get_id_owner_link_for_user(self, id_link: int,) -> int:
        """Повертає id власника URL по id_link
        (для авторизованих користувачів)"""
        return Links.objects.values('owner_id_id').filter(pk=id_link)[0]['owner_id_id']

    def get_link_by_hash(self, hash_url: str) -> str:
        """Повертає Url за переданим hash_url """
        return Links.objects.values('main_links').filter(short_links=hash_url)[0]['main_links']

    def get_idlink_by_hash(self, hash_url: str):
        """Повертає id_url за переданим hash_url"""
        return Links.objects.values('pk').filter(short_links=hash_url)[0]['pk']

    def create_short_url_use_api(self, request, hash_url) -> None:
        """Додає новий запис з довгим та коротким URL в таблицю"""
        Links.objects.create(main_links=request.data['link'], short_links=hash_url)


class ClickToLinks(models.Model):
    id_links = models.ForeignKey('Links', on_delete=models.CASCADE)
    ip_visitor = models.TextField(blank=False)
    id_country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)
    time_visit = models.DateTimeField(auto_now=True)

    def add_new_click(self, ip_visitor: str, id_link: int) -> None:
        """Додає новий запис про клік в таблицю"""
        ClickToLinks.objects.create(ip_visitor=ip_visitor,
                                    id_country_id=None,
                                    id_links_id=id_link)

    def get_count_clicks(self, id_links: int):
        """Повертає кількість переходів по URL """
        clicks = ClickToLinks.objects.filter(
            id_links_id=id_links).values('id_links_id').annotate(clicks=Count('id_links_id'))
        return clicks[0]['clicks']

    def get_guest_by_ip_and_id_link(self, ip_visitor: str, id_link: int):
        """Повертає гостя з полями ip_visitor id_links_id"""
        return ClickToLinks.objects.filter(ip_visitor=ip_visitor, id_links_id=id_link)

    def update_date_last_click(self, ip_visitor: str, id_link: int) -> None:
        """Оновлює дату останього переходу по переданому id_link"""
        ClickToLinks.objects.filter(ip_visitor=ip_visitor, id_links_id=id_link).update(time_visit=datetime.now())


class Country(models.Model):
    name = models.TextField(blank=False)
