# Generated by Django 2.1 on 2018-11-06 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glossario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BarraPesquisa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('barraPesquisaLibras', models.BooleanField(default=True)),
            ],
        ),
    ]
