# Generated by Django 2.2.3 on 2019-09-07 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glossario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sinal',
            name='localizacao',
            field=models.CharField(choices=[('', 'Nenhuma'), ('4', 'Cabeça'), ('12', 'Ombros'), ('3', 'Braços'), ('6', 'Nariz'), ('2', 'Bochechas'), ('1', 'Boca'), ('16', 'Tronco'), ('10', 'Espaço Neutro'), ('11', 'Olhos'), ('17', 'Orelhas'), ('13', 'Pescoço'), ('14', 'Queixo'), ('15', 'Testa'), ('5', 'Mãos')], default='', max_length=2),
        ),
        migrations.AlterUniqueTogether(
            name='sinal',
            unique_together={('portugues', 'glossario', 'ingles', 'cmE', 'cmD', 'localizacao', 'movimentacao')},
        ),
    ]
