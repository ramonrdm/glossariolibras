# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import FileField, DateTimeField
from django.core.files import File
from django.contrib.auth import hashers
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import datetime
import subprocess
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

class UserManagerGlossario(BaseUserManager):
    
    def _create_user(self, email, nome_completo, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, nome_completo=nome_completo, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)

    def create_user(self, email, nome_completo, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', True)

        return self._create_user(email, nome_completo, password, **extra_fields)

    def create_superuser(self, email, password, nome_completo, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, nome_completo, password, **extra_fields)

class UserGlossario(AbstractBaseUser, PermissionsMixin):
    
    class Meta:
        verbose_name = "Usuário"

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    nome_completo = models.CharField(max_length=255, null=False)
    email_confirmed = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    objects = UserManagerGlossario()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_completo']

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def update_user_profile(sender, instance, created, **extra_fields):
        if created:
            UserGlossario.objects.create_user(user=instance)
        instance.save()

    def __str__(self):
        return self.email

class Video(FileField):
    capa = models.ImageField(blank=True)
    videoMp4 = models.FileField()

class Glossario(models.Model):

    class Meta:
        verbose_name='Glossário'

    nome = models.CharField('Nome do Glossário', max_length=100)
    responsavel = models.ManyToManyField(UserGlossario, verbose_name = 'responsável')
    membros = models.ManyToManyField(UserGlossario, related_name='glossario_membros', verbose_name='membros', blank=True)
    descricao = models.TextField("descrição", default='')
    imagem = models.ImageField('Imagem', blank =True)
    link = models.CharField('Link', max_length=20)
    dataCriacao = models.DateField('data de criação', auto_now_add=True)
    videoGlossario = Video('Vídeo', blank=True)

    def __str__(self):
        return self.nome

class CM (models.Model):
    class Meta:
        verbose_name_plural='configurações de mão'

    bsw = models.TextField('BSW', blank=True, default='')
    imagem = models.ImageField(blank=True)

    def __str__(self):
        return str(self.id)

class Tema(models.Model):
    nome = models.CharField('Nome', max_length=30)
    descricao = models.CharField('Descrição', max_length=100, null=True)
    video = Video('Vídeo', null=True, blank=True)
    imagem = models.ImageField('Imagem', blank=False, null=True)
    temaPai = models.ForeignKey('self',null=True, blank = True, verbose_name = 'Tema Pai', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

def sinal_upload_path(instance, filename):
    # o arquivo será salvo em MEDIA_ROOT/sinal_videos/originais/<filename>
    return 'sinal_videos/originais/{0}'.format(filename)

class Sinal(models.Model):
    class Meta:
        verbose_name_plural = 'sinais'
        unique_together = ('traducaoP', 'traducaoI', 'cmE','cmD', 'localizacao', 'movimentacao')

    glossario = models.ForeignKey(Glossario, verbose_name='glossário', null=True, on_delete=models.CASCADE)
    traducaoP = models.CharField('palavra', max_length=30)
    traducaoI = models.CharField('word', max_length=30)
    bsw = models.TextField(null=True, blank=True)
    descricao = models.TextField('descrição',  null=True)
    cmE = models.ForeignKey(CM, related_name='C_M_Esquerda', verbose_name='configuração da mão esquerda', on_delete=models.CASCADE)
    cmD = models.ForeignKey(CM, related_name='C_M_Direita', verbose_name='configuração da mão direita', on_delete=models.CASCADE)
    localizacoes = (('0','Nunhuma'),('1','Cabeça'),('2','Ombros'),('3','Braços'),('4','Nariz'),('5','Bochechas'),
                        ('6','Boca'),('7','Tronco'),('8','Espaço Neutro'),('9','Olhos'),('10','Orelhas'),
                        ('11','Pescoço'),('12','Queixo'),('13','Testa')
                    )
    localizacao = models.CharField(max_length=2, choices=localizacoes,default=0)
    movimentacoes = (('0', 'Sem Movimentação'),('1', 'Parede'), ('2', 'Chão'), ('3', 'Circular'), ('4', 'Contato'))
    movimentacao = models.CharField(max_length=10, choices=movimentacoes, default=0)
    create_data = models.DateTimeField(auto_now_add=True)
    postador = models.ForeignKey(UserGlossario, null=True, on_delete=models.CASCADE)
    publicado = models.BooleanField(default=False)
    sinalLibras = Video('Vídeo do sinal', upload_to=sinal_upload_path, null=True, blank=True)
    preview = models.ImageField('Preview do Video de sinal', null=True)
    descLibras = Video('Vídeo da descrição', upload_to=sinal_upload_path, null=True, blank=True)
    exemploLibras = Video('Vídeo do exemplo', upload_to=sinal_upload_path, null=True, blank=True)
    varicLibras = Video('Vídeo da variante', upload_to=sinal_upload_path, null=True, blank=True)
    tema = models.ForeignKey(Tema, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.traducaoP

@receiver(post_save, sender=Sinal)
def update_upload_path(sender, instance, created, **kwargs):
    # o arquivo será salvo em MEDIA_ROOT/sinal_videos/convertidos/<id>-<tag>-<YYYY>-<MM>-<DD>-<HH><MM><SS>

    originais = '{0}/sinal_videos/originais'.format(settings.MEDIA_ROOT)
    convertidos = '{0}/sinal_videos/convertidos'.format(settings.MEDIA_ROOT)

    videoFields = [instance.sinalLibras, instance.descLibras, instance.exemploLibras, instance.varicLibras]
    tags = ['sinal', 'descricao', 'exemplo', 'variacao']

    for index, field in enumerate(videoFields):
        if field:
            subprocess.call('ffmpeg -i {0}/{1} -c:v libx264 -crf 19 -movflags faststart -threads 0 -preset slow -c:a aac -strict -2 {2}/{3}-{4}-%s.mp4'
                .format(
                    originais,
                    str(field).split('/')[2],
                    convertidos,
                    instance.id,
                    tags[index]
                    )
                    % datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
                    shell=True
                    )
