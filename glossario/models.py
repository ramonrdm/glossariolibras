# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import FileField
from django.core.files import File
from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from django.contrib.auth import hashers
from django.db.models.signals import post_save
import datetime
from django.dispatch import receiver

class UsuarioManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, username, email, password, **extra_fields):
		if not username:
			raise ValueError('Este campo é obrigatório')
		email = self.normalize_email(email)
		user = self.model(username=username, email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, username, email=None, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(username, email, password, **extra_fields)

	def create_superuser(self, username, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Não é membro da equipe.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Não é superusuario.')

		return self._create_user(username, email, password, **extra_fields)



class Usuario(AbstractUser):

	nome = models.CharField('Nome', max_length=200)
	latte = models.CharField('Currículo Latte', max_length=300)
	foto = models.ImageField('Foto', blank=True)

	objects = UsuarioManager()


class Localizacao(models.Model):
	class Meta:
		verbose_name_plural='localizações'

	nome = models.CharField('Nome', max_length=30)
	bsw = models.TextField('BSW')
	imagem = models.ImageField('Imagem', blank=True)
	areaClicavel = models.TextField()

	def __unicode__(self):
		return self.nome

class Video(FileField):
	capa = models.ImageField(blank=True)
	videoMp4 = models.FileField()

class Glossario(models.Model):
	class Meta:
		verbose_name='glossário'

	nome = models.CharField('Nome do Glossário', max_length=100)
	responsavel = models.ManyToManyField(Usuario, verbose_name = 'responsável')
	membros = models.ManyToManyField(Usuario, related_name='glossario_membros', verbose_name='membros', blank=True)
	imagem = models.ImageField('Imagem', blank=True)
	link = models.CharField('Link', max_length=20)
	dataCriacao = models.DateField('data de criação', auto_now_add=True)
	videoGlossario = Video('Vídeo', blank=True)

	def __unicode__(self):
		return self.nome

class GrupoCM (models.Model):
	class Meta:
		verbose_name_plural='Grupos de configuração de mão'

	imagem = models.ImageField(blank=True)
	bsw = models.TextField('BSW')

	def __str__(self):
		return self.bsw

class CM (models.Model):
	class Meta:
		verbose_name_plural='configurações de mão'

	bsw = models.TextField('BSW', blank=True, default='')
	imagem = models.ImageField(blank=True)
	grupo = models.ForeignKey(GrupoCM, verbose_name = 'Grupo de Configuração de Mão')


	def __str__(self):
		return str(self.bsw)+" - "+str(self.grupo)


class Tema(models.Model):
	nome = models.CharField('Nome', max_length=30)
	descricao = models.CharField('Descrição', max_length=100, null=True)
	video = Video('Vídeo', null=True, blank=True)
	imagem = models.ImageField('Imagem', blank=True, null=True)
	temaPai = models.ForeignKey('self',null=True, blank = True, verbose_name = 'Tema Pai')

	def __unicode__(self):
		return self.nome

class Sinal(models.Model):
	class Meta:
		verbose_name_plural='sinais'

	glossario = models.ForeignKey(Glossario, verbose_name = 'glossário')
	traducaoP = models.CharField('palavra', max_length=30)
	traducaoI = models.CharField('word', max_length=30)
	bsw = models.TextField(null=True, blank = True)
	descricao = models.CharField('descrição', max_length=50,null=True, blank = True)
	grupoCMe = models.ForeignKey(GrupoCM, related_name='Grupo_M_Esquerda', verbose_name='grupo configuração de mão esquerda')
	cmE = models.ForeignKey(CM, related_name='C_M_Esquerda', verbose_name='configuração esquerda')
	grupoCMd = models.ForeignKey(GrupoCM, related_name='Grupo_M_Direita', verbose_name='grupo configuração de mão direita')
	cmD = models.ForeignKey(CM, related_name='C_M_Direita', verbose_name='configuração direita')
	localizacao = models.ForeignKey(Localizacao,null=True, blank = True, verbose_name='localização')
	dataPost = models.DateField('data de criação')
	postador = models.ForeignKey(Usuario)
	publicado = models.BooleanField(default=False)
	sinalLibras = Video('Vídeo do Sinal',null=True, blank = True)
	descLibras = Video('Vídeo da Descrição',null=True, blank = True)
	exemploLibras = Video('Vídeo do Exemplo',null=True, blank = True)
	varicLibras = Video('Vídeo da Variação',null=True, blank = True)
	tema = models.ForeignKey(Tema)

	def __unicode__(self):
		return  self.traducaoP