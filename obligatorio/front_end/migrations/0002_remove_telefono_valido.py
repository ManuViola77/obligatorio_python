# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-13 13:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telefono',
            name='valido',
        ),
    ]
