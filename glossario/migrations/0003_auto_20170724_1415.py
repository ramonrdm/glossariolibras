# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-24 17:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glossario', '0002_auto_20170724_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='foto',
            field=models.ImageField(blank=True, upload_to=b"{% static 'img/profile_images/' %}"),
        ),
    ]