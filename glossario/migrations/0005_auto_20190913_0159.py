# Generated by Django 2.2.3 on 2019-09-13 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glossario', '0004_auto_20190913_0150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sinal',
            name='ingles',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='word'),
        ),
        migrations.AlterField(
            model_name='sinal',
            name='portugues',
            field=models.CharField(max_length=50, verbose_name='palavra'),
        ),
    ]
