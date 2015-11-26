# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import glossario.models


class Migration(migrations.Migration):

    dependencies = [
        ('glossario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tema',
            name='descricao',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tema',
            name='imagem',
            field=models.ImageField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tema',
            name='temaPai',
            field=models.ForeignKey(to='glossario.Tema', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tema',
            name='video',
            field=glossario.models.Video(null=True, upload_to=b''),
            preserve_default=True,
        ),
    ]
