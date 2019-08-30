# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import FileField, DateTimeField
from django.core.files import File
from django.contrib.auth import hashers
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

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
    videoGlossario = FileField('Vídeo', blank=True)
    visivel = models.BooleanField("Visivel", default=True)

    def __str__(self):
        return self.nome

class CM (models.Model):
    """Total de 261 configurações de mão divididas em 10 grupos."""
    class Meta:
        verbose_name_plural='Configurações de Mão'

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
    
    localizacoes = (('0','Nunhuma'),('1','Cabeça'),('2','Ombros'),('3','Braços'),('4','Nariz'),('5','Bochechas'),
                    ('6','Boca'),('7','Tronco'),('8','Espaço Neutro'),('9','Olhos'),('10','Orelhas'),
                    ('11','Pescoço'),('12','Queixo'),('13','Testa')
                )
    localizacoes_imagens = dict(
            [('1', 'localizacaoCabeca.png'), ('2', 'localizacaoOmbros.png'), ('3', 'localizacaoBracos.png'),
             ('4', 'localizacaoNariz.png'), ('5', 'localizacaoBochechas.png'), ('6', 'localizacaoBoca.png'),
             ('7', 'localizacaoTronco.png'), ('8', 'localizacaoNeutro.png'), ('9', 'localizacaoOlhos.png'),
             ('10', 'localizacaoOrelhas.png'),
             ('11', 'localizacaoPescoco.png'), ('12', 'localizacaoQueixo.png'), ('13', 'localizacaoTesta.png')])

        
class Movimentacao(models.Model):
    class Meta:
        abstract = True

    movimentacoes = (('0', 'Sem Movimentação'),('1', 'Parede'), ('2', 'Chão'), ('3', 'Circular'), ('4', 'Contato'))

    movimentacoes_imagens = dict(
        [('0', '0X.svg'), ('1', '1parede.png'), ('2', '2chao.png'), ('3', '3circular.png'), ('4', '4contato.png')])

    movimentacoes_busca = (( '0X.svg'), ('1parede.png'), ('2chao.png'), ('3circular.png'), ('4contato.png'))

class Tema(models.Model):
    nome = models.CharField('Nome', max_length=30)
    descricao = models.CharField('Descrição', max_length=100, null=True)
    video = FileField('Vídeo', null=True, blank=True)
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
    
    original_mode = None

    def __init__(self, *args, **kwargs):
        super(Sinal, self).__init__(*args, **kwargs)
        self.original_mode = self.sinalLibras

    glossario = models.ForeignKey(Glossario, verbose_name='glossário', null=True, on_delete=models.CASCADE)
    traducaoP = models.CharField('palavra', max_length=30)
    traducaoI = models.CharField('word', max_length=30)
    bsw = models.TextField(null=True, blank=True)
    descricao = models.TextField('descrição',  null=True)
    cmE = models.ForeignKey(CM, related_name='C_M_Esquerda', verbose_name='configuração da mão esquerda', on_delete=models.CASCADE)
    cmD = models.ForeignKey(CM, related_name='C_M_Direita', verbose_name='configuração da mão direita', on_delete=models.CASCADE)
    localizacao = models.CharField(max_length=2, choices=Localizacao.localizacoes, default=0)
    movimentacao = models.CharField(max_length=10, choices=Movimentacao.movimentacoes, default=0)
    create_data = models.DateTimeField(auto_now_add=True)
    postador = models.ForeignKey(UserGlossario, null=True, on_delete=models.CASCADE)
    publicado = models.BooleanField(default=False)
    sinalLibras = FileField('Vídeo do sinal', upload_to=sinal_upload_path, null=True, blank=True)
    descLibras = FileField('Vídeo da descrição', upload_to=sinal_upload_path, null=True, blank=True)
    exemploLibras = FileField('Vídeo do exemplo', upload_to=sinal_upload_path, null=True, blank=True)
    varicLibras = FileField('Vídeo da variante', upload_to=sinal_upload_path, null=True, blank=True)
    tema = models.ForeignKey(Tema, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.traducaoP
