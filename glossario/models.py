# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import FileField
from django.core.files import File
from django.contrib.auth.models import User
import datetime

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
	responsavel = models.ForeignKey(User)
	imagem = models.ImageField(blank=True)
	link = models.CharField(max_length=20)
	dataCriacao = models.DateField(auto_now_add=True)

	def __unicode__(self):
		return self.nome

class GrupoCM (models.Model):
	imagem = models.ImageField(blank=True)
	bsw = models.TextField()

class CM (models.Model):
	imagem = models.ImageField(blank=True)
	grupo = models.ForeignKey(GrupoCM)


class Sinal(models.Model):
	glossario = models.ForeignKey(Glossario)
	traducaoP = models.CharField(max_length=30)
	traducaoI = models.CharField(max_length=30)
	bsw = models.TextField()
	descricao = models.CharField(max_length=50)
	grupoCMe = models.ForeignKey(GrupoCM, related_name='Grupo_M_Esquerda')
	cmE = models.ForeignKey(CM, related_name='C_M_Esquerda')
	grupoCMd = models.ForeignKey(GrupoCM, related_name='Grupo_M_Direita')
	cmD = models.ForeignKey(CM, related_name='C_M_Direita')
	localizacao = models.ForeignKey(Localizacao)
	dataPost = models.DateField()
	postador = models.ForeignKey(User)
	publicado = models.BooleanField(default=False)
	sinalLibras = Video()
	descLibras = Video()
	exemploLibras = Video()
	varicLibras = Video()