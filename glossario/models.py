# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import FileField, DateTimeField
from django.core.files import File
from django.contrib.auth import hashers
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from model_utils.managers import InheritanceManager


class UserManagerGlossario(BaseUserManager):
    def _create_user(self, email, nome_completo, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(
            email=email, nome_completo=nome_completo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

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

    def email_user(self, subject, message, from_email, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [
            self.email], fail_silently=False, **kwargs)

    def __str__(self):
        return self.nome_completo


class AreaConhecimento(models.Model):
    class Meta:
        verbose_name = 'Área do Conhecimento'

    areas = [('0', 'Superior'), ('1', 'Fundamental')]

class Glossario(models.Model):

    class Meta:
        verbose_name = 'Glossário'
        ordering = ['nome']
        # unique_together = ('nome', 'area')

    objects = InheritanceManager()

    max_length_name = 100
    nome = models.CharField('Nome do Glossário', max_length=max_length_name, unique=True,
                            error_messages={'unique': "Um glossário com este nome já existe."})
    responsaveis = models.ManyToManyField(
        UserGlossario, verbose_name='responsaveis')
    membros = models.ManyToManyField(
        UserGlossario, related_name='glossario_membros', verbose_name='membros', blank=True)
    descricao = models.TextField("descrição", blank=True, null=True)
    imagem = models.ImageField('Imagem', blank=True)
    link = models.CharField('Link', max_length=max_length_name)
    data_criacao = models.DateField('data de criação', auto_now_add=True)
    video = FileField('Vídeo', blank=True)
    visivel = models.BooleanField("Visivel", default=True)

    area = models.CharField(max_length=20, choices=AreaConhecimento.areas, default='')

    def sinais_number(self):
        return Sinal.objects.filter(publicado=True, glossario=self).count()

    def clean(self):
        self.nome = self.nome.title()

    def __str__(self):
        return self.nome.title()

class GrupoGlossarios(Glossario):
    grupo_de_glossarios = models.ManyToManyField(Glossario, related_name='grupo_de_glossarios', blank=True)

    def sinais_number(self):
        num_sinais = Sinal.objects.filter(publicado=True, glossario=self).count()
        for glossario in self.grupo_de_glossarios.all():
            num_sinais += Sinal.objects.filter(publicado=True, glossario=glossario).count()
        return num_sinais
            

class CM (models.Model):
    """Total de 261 configurações de mão divididas em 10 grupos."""
    class Meta:
        verbose_name_plural = 'Configurações de Mão'

    bsw = models.TextField('BSW', blank=True, default='0')
    name = models.TextField('name', default='')
    group = models.TextField('Grupo', default='')

    def imagem(self):
        return str(""+str(self.group)+"/"+self.bsw+".png")

    def __str__(self):
        return str(str(self.id)+" "+self.bsw)


class Localizacao(models.Model):
    class Meta:
        abstract = True

    localizacoes = (('0', 'Nenhuma'), ('4', 'Cabeça'), ('12', 'Ombros'), ('3', 'Braços'),
                    ('6', 'Nariz'), ('2', 'Bochechas'), ('1', 'Boca'), ('16', 'Tronco'),
                    ('10', 'Espaço Neutro'), ('11', 'Olhos'), ('17', 'Orelhas'),
                    ('13', 'Pescoço'), ('14', 'Queixo'), ('15', 'Testa'),
                    ('5', 'Mãos')
                    )
    localizacoes_imagens = dict(
        [('0', '0.png'), ('4', 'localizacaoCabeca.png'), ('12', 'localizacaoOmbros.png'),
         ('3', 'localizacaoBracos.png'), ('6', 'localizacaoNariz.png'), ('2','localizacaoBochechas.png'),
         ('1', 'localizacaoBoca.png'), ('16', 'localizacaoTronco.png'), ('10', 'localizacaoNeutro.png'),
         ('11', 'localizacaoOlhos.png'), ('17', 'localizacaoOrelhas.png'), ('13','localizacaoPescoco.png'),
         ('14', 'localizacaoQueixo.png'), ('15', 'localizacaoTesta.png'), ('5', 'localizacaoMaos.png')])

class Movimentacao(models.Model):
    class Meta:
        abstract = True

    movimentacoes = (('0', 'Sem Movimentação'), ('1', 'Parede'),
                     ('2', 'Chão'), ('3', 'Circular'), ('4', 'Contato'))

    movimentacoes_imagens = dict(
        [('0', '0.png'), ('1', '1parede.png'), ('2', '2chao.png'), ('3', '3circular.png'), ('4', '4contato.png')])

def sinal_upload_path(instance, filename):
    # o arquivo será salvo em MEDIA_ROOT/sinal_videos/originais/<filename>
    return 'sinal_videos/{0}'.format(filename)


def preview_upload_path(instance, filename):
    return 'sinal_preview/{0}'.format(filename)


class Sinal(models.Model):
    class Meta:
        verbose_name_plural = 'sinais'
        ordering = ['portugues']

    videos_originais_converter = []

    def __init__(self, *args, **kwargs):
        super(Sinal, self).__init__(*args, **kwargs)
        self.videos_originais_converter = [
            self.video_sinal, self.video_descricao, self.video_exemplo, self.video_variacao]

    glossario = models.ForeignKey(
        Glossario, verbose_name='glossário', null=True, on_delete=models.CASCADE)
    portugues = models.CharField('palavra', max_length=50)
    ingles = models.CharField('word', blank=True, null=True, max_length=50)
    bsw = models.TextField(null=True, blank=True)
    descricao = models.TextField('descrição',  blank=True, null=True)
    cmE = models.ForeignKey(CM, related_name='C_M_Esquerda', verbose_name='configuração da mão esquerda',
                            blank=True, null=True, on_delete=models.CASCADE, default='')
    cmD = models.ForeignKey(CM, related_name='C_M_Direita', verbose_name='configuração da mão direita',
                            blank=True, null=True, on_delete=models.CASCADE, default='')
    localizacao = models.CharField('Localização',
        max_length=2, choices=Localizacao.localizacoes, blank=True, null=True, default='')
    movimentacao = models.CharField('Movimento',
        max_length=10, choices=Movimentacao.movimentacoes, blank=True, null=True, default='')
    data_criacao = models.DateTimeField(auto_now_add=True)
    postador = models.ForeignKey(UserGlossario, on_delete=models.CASCADE)
    publicado = models.BooleanField(default=False)
    video_sinal = FileField(
        'Vídeo do sinal', upload_to=sinal_upload_path, null=True)
    video_descricao = FileField(
        'Vídeo da descrição', upload_to=sinal_upload_path, null=True, blank=True)
    video_exemplo = FileField(
        'Vídeo do exemplo', upload_to=sinal_upload_path, null=True, blank=True)
    video_variacao = FileField(
        'Vídeo de variações', upload_to=sinal_upload_path, null=True, blank=True)
    preview1 = FileField(
        'Preview1', upload_to=preview_upload_path, null=True, blank=True)
    preview2 = FileField(
        'Preview2', upload_to=preview_upload_path, null=True, blank=True)
    preview3 = FileField(
        'Preview3', upload_to=preview_upload_path, null=True, blank=True)
    preview4 = FileField(
        'Preview4', upload_to=preview_upload_path, null=True, blank=True)

    def __str__(self):
        return self.portugues

    def localizacao_imagem(self):
        return str("/static/img/" + Localizacao.localizacoes_imagens[self.localizacao])
    
    def movimentacao_imagem(self):
        return str("/static/img/" + Movimentacao.movimentacoes_imagens[self.movimentacao])

    def save(self, *args, **kwargs):
        url_base = settings.MEDIA_ROOT
        pasta_sinal_preview = '{0}/sinal_preview'.format(url_base)
        pasta_sinal_videos = '{0}/sinal_videos'.format(url_base)
        super().save(*args, **kwargs)
