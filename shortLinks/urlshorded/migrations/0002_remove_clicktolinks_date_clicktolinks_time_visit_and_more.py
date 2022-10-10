# Generated by Django 4.1.2 on 2022-10-09 22:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urlshorded', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clicktolinks',
            name='date',
        ),
        migrations.AddField(
            model_name='clicktolinks',
            name='time_visit',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 9, 22, 49, 34, 644812)),
        ),
        migrations.AlterField(
            model_name='links',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]