# Generated by Django 2.1 on 2018-10-30 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import glossario.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGlossario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('nome_completo', models.CharField(max_length=255)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bsw', models.TextField(blank=True, default='', verbose_name='BSW')),
                ('imagem', models.ImageField(blank=True, upload_to='')),
            ],
            options={
                'verbose_name_plural': 'configurações de mão',
            },
        ),
        migrations.CreateModel(
            name='Glossario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome do Glossário')),
                ('descricao', models.TextField(default='', verbose_name='descrição')),
                ('imagem', models.ImageField(blank=True, upload_to='', verbose_name='Imagem')),
                ('link', models.CharField(max_length=20, verbose_name='Link')),
                ('dataCriacao', models.DateField(auto_now_add=True, verbose_name='data de criação')),
                ('videoGlossario', glossario.models.Video(blank=True, upload_to='', verbose_name='Vídeo')),
                ('membros', models.ManyToManyField(blank=True, related_name='glossario_membros', to=settings.AUTH_USER_MODEL, verbose_name='membros')),
                ('responsavel', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='responsável')),
            ],
            options={
                'verbose_name': 'Glossário',
            },
        ),
        migrations.CreateModel(
            name='GrupoCM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(blank=True, upload_to='')),
                ('bsw', models.TextField(verbose_name='BSW')),
            ],
            options={
                'verbose_name_plural': 'Grupos de configuração de mão',
            },
        ),
        migrations.CreateModel(
            name='Sinal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('traducaoP', models.CharField(max_length=30, verbose_name='palavra')),
                ('traducaoI', models.CharField(max_length=30, verbose_name='word')),
                ('bsw', models.TextField(blank=True, null=True)),
                ('descricao', models.CharField(max_length=200, null=True, verbose_name='descrição')),
                ('localizacao', models.CharField(choices=[('1', 'Cabeça'), ('2', 'Ombros'), ('3', 'Braços'), ('4', 'Nariz'), ('5', 'Bochechas'), ('6', 'Boca'), ('7', 'Tronco'), ('8', 'Espaço Neutro'), ('9', 'Olhos'), ('10', 'Orelhas'), ('11', 'Pescoço'), ('12', 'Queixo'), ('13', 'Testa')], default=8, max_length=2)),
                ('movimentacao', models.CharField(choices=[('sem', 'Sem Movimentação'), ('parede', 'Parede'), ('chao', 'Chão'), ('circular', 'Circular'), ('contato', 'Contato')], default='sem', max_length=10)),
                ('dataPost', models.DateField(null=True, verbose_name='data de criação')),
                ('publicado', models.BooleanField(default=False)),
                ('sinalLibras', glossario.models.Video(blank=True, null=True, upload_to=glossario.models.sinal_upload_path, verbose_name='Vídeo do sinal')),
                ('descLibras', glossario.models.Video(blank=True, null=True, upload_to=glossario.models.sinal_upload_path, verbose_name='Vídeo da descrição')),
                ('exemploLibras', glossario.models.Video(blank=True, null=True, upload_to=glossario.models.sinal_upload_path, verbose_name='Vídeo do exemplo')),
                ('varicLibras', glossario.models.Video(blank=True, null=True, upload_to=glossario.models.sinal_upload_path, verbose_name='Vídeo da variante')),
                ('cmD', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='C_M_Direita', to='glossario.CM', verbose_name='configuração da mão direita')),
                ('cmE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='C_M_Esquerda', to='glossario.CM', verbose_name='configuração da mão esquerda')),
                ('glossario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='glossario.Glossario', verbose_name='glossário')),
                ('grupoCMd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Grupo_M_Direita', to='glossario.GrupoCM', verbose_name='grupo da mão direita')),
                ('grupoCMe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Grupo_M_Esquerda', to='glossario.GrupoCM', verbose_name='grupo da mão esquerda')),
                ('postador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'sinais',
            },
        ),
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30, verbose_name='Nome')),
                ('descricao', models.CharField(max_length=100, null=True, verbose_name='Descrição')),
                ('video', glossario.models.Video(blank=True, null=True, upload_to='', verbose_name='Vídeo')),
                ('imagem', models.ImageField(null=True, upload_to='', verbose_name='Imagem')),
                ('temaPai', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='glossario.Tema', verbose_name='Tema Pai')),
            ],
        ),
        migrations.AddField(
            model_name='sinal',
            name='tema',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='glossario.Tema'),
        ),
        migrations.AddField(
            model_name='cm',
            name='grupo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='glossario.GrupoCM', verbose_name='Grupo de Configuração de Mão'),
        ),
        migrations.AlterUniqueTogether(
            name='sinal',
            unique_together={('traducaoP', 'traducaoI', 'grupoCMe', 'cmE', 'grupoCMd', 'cmD', 'localizacao')},
        ),
    ]
