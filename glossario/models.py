# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import FileField
from django.core.files import File
from django.contrib.auth.models import User

class Localizacao(models.Model):
	nome = models.CharField(max_length=30)
	bsw = models.TextField()

class Video(FileField):
	capa = models.ImageField(blank=True)
	videoMp4 = models.FileField()

class Glossario(models.Model):
	nome = models.CharField(max_length=100)
	responsavel = models.ForeignKey(User)
	#imgagem = models.ImageField(blank=True)

class Sinal(models.Model):
	glossario = models.ForeignKey(Glossario)
	traducaoP = models.CharField(max_length=30)
	traducaoI = models.CharField(max_length=30)
	bsw = models.TextField()
	descricao = models.CharField(max_length=50)
	localizacao = models.ForeignKey(Localizacao)
	dataPost = models.DateField()
	postador = models.ForeignKey(User)
	publicado = models.BooleanField(default=False)
	sinalLibras = Video()
	descLibras = Video()
	exemploLibras = Video()
	varicLibras = Video()

class GrupoCM (models.Model):
	imagem = models.ImageField(blank=True)
	bsw = models.TextField()

class CM (models.Model):
	imagem = models.ImageField(blank=True)
	grupo = models.ForeignKey(GrupoCM)
