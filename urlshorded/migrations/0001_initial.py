# Generated by Django 4.1.2 on 2022-10-11 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Guests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_links', models.TextField()),
                ('short_links', models.TextField()),
                ('deleted', models.BooleanField(default=False)),
                ('owner_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('owner_ip', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='urlshorded.guests')),
            ],
        ),
        migrations.CreateModel(
            name='ClickToLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_visitor', models.TextField()),
                ('time_visit', models.DateTimeField(auto_now=True)),
                ('id_country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='urlshorded.country')),
                ('id_links', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urlshorded.links')),
            ],
        ),
    ]
