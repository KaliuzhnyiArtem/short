from django.db import models
from django.db.models import Count
from datetime import datetime


class UserInfo(models.Model):
    username = models.TextField()
    password = models.TextField()


class Guests(models.Model):
    ip = models.TextField()

    def get_id_guests(self, ip_guest):
        id_guest = Guests.objects.filter(ip=ip_guest)[0].pk
        if id_guest:
            return id_guest


class Links(models.Model):
    main_links = models.TextField(blank=False)
    short_links = models.TextField(blank=False)
    deleted = models.BooleanField(default=False)
    owner_id = models.ForeignKey('UserInfo', on_delete=models.PROTECT, null=True)
    owner_ip = models.ForeignKey('Guests', on_delete=models.PROTECT, null=True)

    def get_guest_data(self, ip):
        guest = Guests()
        id_guest = guest.get_id_guests(ip)
        list_items = Links.objects.raw(
            f'SELECT *, (SELECT  count(id_links_id) FROM  urlshorded_clicktolinks WHERE id_links_id=urlshorded_links.id GROUP BY (id_links_id))  as cliks, (SELECT time_visit FROM urlshorded_clicktolinks WHERE id_links_id=urlshorded_links.id ORDER BY time_visit DESC LIMIT 1) as time_visit  FROM urlshorded_links WHERE (owner_ip_id={id_guest} AND  deleted=False) ORDER BY id DESC'
        )

        # return Links.objects.filter(owner_ip_id=id_guest, deleted=False).order_by('-pk')
        return list_items

    def get_user_data(self):
        return Links.objects.filter(owner_id_id=1)

    def valid_hash(self, url_hash):
        if Links.objects.filter(short_links=url_hash):
            return False
        else:
            return True

    def add_new_link(self, link, hash, owner_ip):
        guest = Guests()
        id_guest = guest.get_id_guests(owner_ip)
        Links.objects.create(main_links=link, short_links=hash, owner_ip_id=id_guest)

    def delete_link(self, id_link):
        Links.objects.filter(pk=id_link).update(deleted=True)

    def validation_access_guest(self, link_id, ip_guest):
        guest = Guests()
        owner_link = Links.objects.values('owner_ip_id').filter(pk=link_id)[0]['owner_ip_id']

        if owner_link == guest.get_id_guests(ip_guest):
            return True
        else:
            return False

    def get_link_by_hash(self, hash_url):
        return Links.objects.values('main_links').filter(short_links=hash_url)[0]['main_links']

    def get_idlink_by_hash(self, hash_url):
        return Links.objects.values('pk').filter(short_links=hash_url)[0]['pk']



class ClickToLinks(models.Model):
    id_links = models.ForeignKey('Links', on_delete=models.PROTECT)
    ip_visitor = models.TextField(blank=False)
    id_country = models.ForeignKey('Country', on_delete=models.PROTECT)
    time_visit = models.DateTimeField(auto_now=True)

    def add_new_click(self, ip_visitor, hash_url):
        link_con = Links()
        id_link = link_con.get_idlink_by_hash(hash_url)
        ClickToLinks.objects.create(ip_visitor=ip_visitor, id_country_id=1, id_links_id=id_link)

    def get_count_clicks(self, id_links):
        clicks = ClickToLinks.objects.filter(
            id_links_id=id_links).values('id_links_id').annotate(clicks=Count('id_links_id'))
        return clicks[0]['clicks']

    def valid_guest(self, ip_visitor, hash_url):
        link_con = Links()
        id_link = link_con.get_idlink_by_hash(hash_url)
        guest = ClickToLinks.objects.filter(ip_visitor=ip_visitor, id_links_id=id_link)
        if guest:
            return False
        else:
            return True

    def update_date_last_click(self, ip_visitor, hash_url):
        link_con = Links()
        id_link = link_con.get_idlink_by_hash(hash_url)
        ClickToLinks.objects.filter(ip_visitor='127.0.0.1', id_links_id=id_link).update(time_visit=datetime.now())


class Country(models.Model):
    name = models.TextField(blank=False)
