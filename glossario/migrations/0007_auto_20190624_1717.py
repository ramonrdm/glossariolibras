# Generated by Django 2.2 on 2019-06-24 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('glossario', '0006_auto_20190506_1434'),
    ]

    operations = [
        # migrations.DeleteModel(
        #     name='BarraPesquisa',
        # ),
        migrations.AlterModelOptions(
            name='userglossario',
            options={'verbose_name': 'Usuário'},
        ),
    ]
