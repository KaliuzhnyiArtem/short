from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from datetime import datetime
from django.conf import settings


class Guests(models.Model):
    ip = models.TextField()

    def get_id_guests(self, ip_guest: str):
        id_guest = Guests.objects.filter(ip=ip_guest)
        if id_guest:
            return id_guest[0].pk


class Links(models.Model):
    main_links = models.TextField(blank=False)
    short_links = models.TextField(blank=False)
    deleted = models.BooleanField(default=False)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    owner_ip = models.ForeignKey('Guests', on_delete=models.PROTECT, null=True)

    def get_guest_data(self, ip='127.0.0.1'):
        guest = Guests()
        id_guest = guest.get_id_guests(ip)
        list_items = Links.objects.raw(
            f'SELECT *, (SELECT  count(id_links_id) FROM  urlshorded_clicktolinks WHERE id_links_id=urlshorded_links.id GROUP BY (id_links_id))  as cliks, (SELECT time_visit FROM urlshorded_clicktolinks WHERE id_links_id=urlshorded_links.id ORDER BY time_visit DESC LIMIT 1) as time_visit  FROM urlshorded_links WHERE (owner_ip_id={id_guest} AND  deleted=False) ORDER BY id DESC'
        )
        return list_items

    def get_user_data(self, id_user: int):
        list_items = Links.objects.raw(
            f'SELECT *, (SELECT  count(id_links_id) FROM  urlshorded_clicktolinks WHERE id_links_id=urlshorded_links.id GROUP BY (id_links_id))  as cliks, (SELECT time_visit FROM urlshorded_clicktolinks WHERE id_links_id=urlshorded_links.id ORDER BY time_visit DESC LIMIT 1) as time_visit  FROM urlshorded_links WHERE (owner_id_id={id_user} AND  deleted=False) ORDER BY id DESC'
        )
        return list_items

    def valid_hash(self, url_hash: str):
        if Links.objects.filter(short_links=url_hash):
            return False
        else:
            return True

    def add_new_link_guest(self, link: str, hash_url: str, owner_ip: str):
        guest = Guests()
        id_guest = guest.get_id_guests(owner_ip)

        Links.objects.create(main_links=link, short_links=hash_url, owner_ip_id=id_guest)

    def add_new_link_user(self, link: str, hash_url, user_id: str):
        Links.objects.create(main_links=link, short_links=hash_url, owner_id_id=user_id)

    def delete_link(self, id_link: int):
        Links.objects.filter(pk=id_link).update(deleted=True)

    def validation_access_guest(self, link_id: int, ip_guest: str):
        guest = Guests()
        owner_link = Links.objects.values('owner_ip_id').filter(pk=link_id)[0]['owner_ip_id']

        if owner_link == guest.get_id_guests(ip_guest):
            return True
        else:
            return False

    def validation_access_user(self, user_id: int, id_link: int, ):
        owner_link = Links.objects.values('owner_id_id').filter(pk=id_link)[0]['owner_id_id']

        if owner_link == user_id:
            return True
        else:
            return False

    def get_link_by_hash(self, hash_url: str):
        return Links.objects.values('main_links').filter(short_links=hash_url)[0]['main_links']

    def get_idlink_by_hash(self, hash_url: str):
        return Links.objects.values('pk').filter(short_links=hash_url)[0]['pk']


class ClickToLinks(models.Model):
    id_links = models.ForeignKey('Links', on_delete=models.PROTECT)
    ip_visitor = models.TextField(blank=False)
    id_country = models.ForeignKey('Country', on_delete=models.PROTECT)
    time_visit = models.DateTimeField(auto_now=True)

    def add_new_click(self, ip_visitor: str, hash_url: str):
        link_con = Links()
        id_link = link_con.get_idlink_by_hash(hash_url)
        ClickToLinks.objects.create(ip_visitor=ip_visitor, id_country_id=1, id_links_id=id_link)

    def get_count_clicks(self, id_links: int):
        clicks = ClickToLinks.objects.filter(
            id_links_id=id_links).values('id_links_id').annotate(clicks=Count('id_links_id'))
        return clicks[0]['clicks']

    def valid_guest(self, ip_visitor: str, hash_url: str):
        link_con = Links()
        id_link = link_con.get_idlink_by_hash(hash_url)
        guest = ClickToLinks.objects.filter(ip_visitor=ip_visitor, id_links_id=id_link)
        if guest:
            return False
        else:
            return True

    def update_date_last_click(self, ip_visitor: int, hash_url: str):
        link_con = Links()
        id_link = link_con.get_idlink_by_hash(hash_url)
        ClickToLinks.objects.filter(ip_visitor=ip_visitor, id_links_id=id_link).update(time_visit=datetime.now())


class Country(models.Model):
    name = models.TextField(blank=False)
