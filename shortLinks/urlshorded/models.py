from django.db import models


class UserInfo(models.Model):
    username = models.TextField()
    password = models.TextField()


class Guests(models.Model):
    ip = models.TextField()


class Links(models.Model):
    main_links = models.TextField(blank=False)
    short_links = models.TextField(blank=False)
    deleted = models.BooleanField()
    owner_id = models.ForeignKey('UserInfo', on_delete=models.PROTECT, null=True)
    owner_ip = models.ForeignKey('Guests', on_delete=models.PROTECT, null=True)


class ClickToLinks(models.Model):
    id_links = models.ForeignKey('Links', on_delete=models.PROTECT)
    ip_visitor = models.TextField(blank=False)
    id_country = models.ForeignKey('Country', on_delete=models.PROTECT)
    date = models.DateField()


class Country(models.Model):
    name = models.TextField(blank=False)
