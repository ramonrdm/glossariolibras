from django.db import models
from django.core.files import File

# Create your models here.

class Glossario(models.Model):
	nome = models.CharField(max_length=100)
	grupoUsuarios = ForeignKey(Grupo)

class Sinal(models.Model):
	glossario = models.ForeignKey(Glossario)
	traducaoP = models.CharField(max_length=30)
	traducaoI = models.CharField(max_length=30)
	bsw = models.TextField()
	descricao = models.CharField(max_length=50)
	localizacao = models.ForeignKey(Localizacao)
	dataPost = models.DateField()
	publicado = models.BooleanField()
	videoSinal = models.ForeignKey(Video)
	videoDesc = models.ForeignKey(Video)
	videoExemplo = models.ForeignKey(Video)
	videoVariac = models.ForeignKey(Video)

class Grupo(models.Model):
	nome = models.CharField(max_length=30)

class Localizacao(models.Model):
	nome = models.CharField(max_length=30)
	bsw = models.TextField()