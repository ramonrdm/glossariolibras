# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-24 18:22
from __future__ import unicode_literals

from django.db import migrations, models
import glossario.models


class Migration(migrations.Migration):

    dependencies = [
        ('glossario', '0006_auto_20170724_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='foto',
            field=models.ImageField(blank=True, upload_to=glossario.models.profile_upload_path),
        ),
    ]