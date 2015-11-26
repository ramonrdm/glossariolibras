# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import glossario.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imagem', models.ImageField(upload_to=b'', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Glossario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=100)),
                ('imagem', models.ImageField(upload_to=b'', blank=True)),
                ('link', models.CharField(max_length=20)),
                ('dataCriacao', models.DateField(auto_now_add=True)),
                ('videoGlossario', glossario.models.Video(upload_to=b'', blank=True)),
                ('membros', models.ManyToManyField(related_name=b'glossario_membros', to=settings.AUTH_USER_MODEL)),
                ('responsavel', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GrupoCM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imagem', models.ImageField(upload_to=b'', blank=True)),
                ('bsw', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Localizacao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=30)),
                ('bsw', models.TextField()),
                ('imagem', models.ImageField(upload_to=b'', blank=True)),
                ('areaClicavel', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sinal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('traducaoP', models.CharField(max_length=30, verbose_name=b'Palavra')),
                ('traducaoI', models.CharField(max_length=30, verbose_name=b'Word')),
                ('bsw', models.TextField()),
                ('descricao', models.CharField(max_length=50)),
                ('dataPost', models.DateField()),
                ('publicado', models.BooleanField(default=False)),
                ('sinalLibras', glossario.models.Video(upload_to=b'')),
                ('descLibras', glossario.models.Video(upload_to=b'')),
                ('exemploLibras', glossario.models.Video(upload_to=b'')),
                ('varicLibras', glossario.models.Video(upload_to=b'')),
                ('cmD', models.ForeignKey(related_name=b'C_M_Direita', verbose_name=b'Configura\xc3\xa7\xc3\xa3o direita', to='glossario.CM')),
                ('cmE', models.ForeignKey(related_name=b'C_M_Esquerda', verbose_name=b'Configura\xc3\xa7\xc3\xa3o esquerda', to='glossario.CM')),
                ('glossario', models.ForeignKey(to='glossario.Glossario')),
                ('grupoCMd', models.ForeignKey(related_name=b'Grupo_M_Direita', verbose_name=b'Grupo configura\xc3\xa7\xc3\xa3o direita', to='glossario.GrupoCM')),
                ('grupoCMe', models.ForeignKey(related_name=b'Grupo_M_Esquerda', verbose_name=b'Grupo configura\xc3\xa7\xc3\xa3o esquerda', to='glossario.GrupoCM')),
                ('localizacao', models.ForeignKey(to='glossario.Localizacao')),
                ('postador', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sinal',
            name='tema',
            field=models.ForeignKey(to='glossario.Tema'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cm',
            name='grupo',
            field=models.ForeignKey(to='glossario.GrupoCM'),
            preserve_default=True,
        ),
    ]
