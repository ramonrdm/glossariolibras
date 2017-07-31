# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-24 18:58
from __future__ import unicode_literals

from django.db import migrations
import glossario.models


class Migration(migrations.Migration):

    dependencies = [
        ('glossario', '0007_auto_20170724_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sinal',
            name='descLibras',
            field=glossario.models.Video(blank=True, null=True, upload_to=glossario.models.sinal_upload_path, verbose_name=b'V\xc3\xaddeo da descri\xc3\xa7\xc3\xa3o'),
        ),
        migrations.AlterField(
            model_name='sinal',
            name='exemploLibras',
            field=glossario.models.Video(blank=True, null=True, upload_to=glossario.models.sinal_upload_path, verbose_name=b'V\xc3\xaddeo do exemplo'),
        ),
        migrations.AlterField(
            model_name='sinal',
            name='sinalLibras',
            field=glossario.models.Video(blank=True, null=True, upload_to=glossario.models.sinal_upload_path, verbose_name=b'V\xc3\xaddeo do sinal'),
        ),
        migrations.AlterField(
            model_name='sinal',
            name='varicLibras',
            field=glossario.models.Video(blank=True, null=True, upload_to=glossario.models.sinal_upload_path, verbose_name=b'V\xc3\xaddeo da varia\xc3\xa7\xc3\xa3o'),
        ),
    ]