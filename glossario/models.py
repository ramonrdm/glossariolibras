# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import FileField
from django.core.files import File
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import hashers
from django.db.models.signals import post_save
import datetime

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

	nome = models.CharField(max_length=200, verbose_name = 'Nome')
	latte = models.CharField(max_length=300, verbose_name = 'Currículo Latte')
	foto = models.ImageField(blank=True, verbose_name = 'Foto')

	objects = UsuarioManager()


class Localizacao(models.Model):
	nome = models.CharField(max_length=30, verbose_name = 'Nome')
	bsw = models.TextField(verbose_name ='BSW')
	imagem = models.ImageField(blank=True, verbose_name='Imagem')
	areaClicavel = models.TextField()

class Video(FileField):
	capa = models.ImageField(blank=True)
	videoMp4 = models.FileField()

class Glossario(models.Model):
	nome = models.CharField(max_length=100, verbose_name='Nome do Glossário')
	responsavel = models.ManyToManyField(Usuario, verbose_name = 'Responsável')
	membros = models.ManyToManyField(Usuario, related_name='glossario_membros', verbose_name='Membros')
	imagem = models.ImageField(blank=True, verbose_name='Imagem')
	link = models.CharField(max_length=20, verbose_name = 'Link')
	dataCriacao = models.DateField(auto_now_add=True)
	videoGlossario = Video(blank=True, verbose_name='Vídeo')

	def __unicode__(self):
		return self.nome

class GrupoCM (models.Model):
	imagem = models.ImageField(blank=True)
	bsw = models.TextField(verbose_name = 'BSW')

class CM (models.Model):
	imagem = models.ImageField(blank=True)
	grupo = models.ForeignKey(GrupoCM, verbose_name = 'Grupo de Configuração de Mão')

class Tema(models.Model):
	nome = models.CharField(max_length=30, verbose_name = 'Nome')
	descricao = models.CharField(max_length=100, null=True, verbose_name = 'Descrição')
	video = Video(null=True, blank=True, verbose_name = 'Vídeo')
	imagem = models.ImageField(blank=True, null=True, verbose_name = 'Imagem')
	temaPai = models.ForeignKey('self',null=True, blank = True, verbose_name = 'Tema Pai')

	def __unicode__(self):
		return self.nome

class Sinal(models.Model):
	glossario = models.ForeignKey(Glossario, verbose_name = 'Glossario')
	traducaoP = models.CharField(max_length=30, verbose_name='Palavra')
	traducaoI = models.CharField(max_length=30, verbose_name='Word')
	bsw = models.TextField(null=True, blank = True)
	descricao = models.CharField(max_length=50,null=True, blank = True)
	grupoCMe = models.ForeignKey(GrupoCM, related_name='Grupo_M_Esquerda', verbose_name='Grupo configuração de mão esquerda')
	cmE = models.ForeignKey(CM, related_name='C_M_Esquerda', verbose_name='Configuração esquerda')
	grupoCMd = models.ForeignKey(GrupoCM, related_name='Grupo_M_Direita', verbose_name='Grupo configuração de mão direita')
	cmD = models.ForeignKey(CM, related_name='C_M_Direita', verbose_name='Configuração direita')
	localizacao = models.ForeignKey(Localizacao,null=True, blank = True)
	dataPost = models.DateField()
	postador = models.ForeignKey(Usuario)
	publicado = models.BooleanField(default=False)
	sinalLibras = Video(verbose_name='Vídeo do Sinal',null=True, blank = True)
	descLibras = Video(verbose_name='Vídeo da Descrição',null=True, blank = True)
	exemploLibras = Video(verbose_name='Vídeo do Exemplo',null=True, blank = True)
	varicLibras = Video(verbose_name='Vídeo da Variação',null=True, blank = True)
	tema = models.ForeignKey(Tema)

	def __unicode__(self):
		return  self.traducaoP