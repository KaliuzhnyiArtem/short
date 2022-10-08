# Generated by Django 4.1.2 on 2022-10-06 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.TextField()),
                ('password', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_links', models.TextField()),
                ('short_links', models.TextField()),
                ('deleted', models.BooleanField()),
                ('owner_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='urlshorded.userinfo')),
                ('owner_ip', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='urlshorded.guests')),
            ],
        ),
        migrations.CreateModel(
            name='ClickToLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_visitor', models.TextField()),
                ('date', models.DateField()),
                ('id_country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='urlshorded.country')),
                ('id_links', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='urlshorded.links')),
            ],
        ),
    ]