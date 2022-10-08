from django.db import models


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
        return Links.objects.filter(owner_ip_id=id_guest).order_by('-pk')

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
        Links.objects.filter(pk=id_link).delete()

    def validation_access_guest(self, link_id, ip_guest):
        guest = Guests()
        owner_link = Links.objects.values('owner_ip_id').filter(pk=link_id)[0]['owner_ip_id']

        if owner_link == guest.get_id_guests(ip_guest):
            return True
        else:
            return False


class ClickToLinks(models.Model):
    id_links = models.ForeignKey('Links', on_delete=models.PROTECT)
    ip_visitor = models.TextField(blank=False)
    id_country = models.ForeignKey('Country', on_delete=models.PROTECT)
    date = models.DateField()


class Country(models.Model):
    name = models.TextField(blank=False)
