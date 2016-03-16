# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import FileField
from django.core.files import File
from django.contrib.auth.models import AbstractUser, BaseUserManager
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
		extra_fields.setdefault('is_staff', False)
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

	latte = models.CharField(max_length=300)
	foto = models.ImageField(blank=True)

	objects = UsuarioManager()


class Localizacao(models.Model):
	nome = models.CharField(max_length=30)
	bsw = models.TextField()
	imagem = models.ImageField(blank=True)
	areaClicavel = models.TextField()

class Video(FileField):
	capa = models.ImageField(blank=True)
	videoMp4 = models.FileField()

class Glossario(models.Model):
	nome = models.CharField(max_length=100)
	responsavel = models.ManyToManyField(Usuario)
	membros = models.ManyToManyField(Usuario, related_name='glossario_membros')
	imagem = models.ImageField(blank=True)
	link = models.CharField(max_length=20)
	dataCriacao = models.DateField(auto_now_add=True)
	videoGlossario = Video(blank=True)

	def __unicode__(self):
		return self.nome

class GrupoCM (models.Model):
	imagem = models.ImageField(blank=True)
	bsw = models.TextField()

class CM (models.Model):
	imagem = models.ImageField(blank=True)
	grupo = models.ForeignKey(GrupoCM)

class Tema(models.Model):
	nome = models.CharField(max_length=30)
	descricao = models.CharField(max_length=100, null=True)
	video = Video(null=True)
	imagem = models.ImageField(blank=True, null=True)
	temaPai = models.ForeignKey('self',null=True) 

class Sinal(models.Model):
	glossario = models.ForeignKey(Glossario)
	traducaoP = models.CharField(max_length=30, verbose_name='Palavra')
	traducaoI = models.CharField(max_length=30, verbose_name='Word')
	bsw = models.TextField()
	descricao = models.CharField(max_length=50)
	grupoCMe = models.ForeignKey(GrupoCM, related_name='Grupo_M_Esquerda', verbose_name='Grupo configuração esquerda')
	cmE = models.ForeignKey(CM, related_name='C_M_Esquerda', verbose_name='Configuração esquerda')
	grupoCMd = models.ForeignKey(GrupoCM, related_name='Grupo_M_Direita', verbose_name='Grupo configuração direita')
	cmD = models.ForeignKey(CM, related_name='C_M_Direita', verbose_name='Configuração direita')
	localizacao = models.ForeignKey(Localizacao)
	dataPost = models.DateField()
	postador = models.ForeignKey(Usuario)
	publicado = models.BooleanField(default=False)
	sinalLibras = Video()
	descLibras = Video()
	exemploLibras = Video()
	varicLibras = Video()
	tema = models.ForeignKey(Tema)

	def __unicode__(self):
		return  self.traducaoP