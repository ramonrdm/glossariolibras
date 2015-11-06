from django.db import models
from django.core.files import File
from django.contrib.auth.models import User

# Create your models here.
class Localizacao(models.Model):
	nome = models.CharField(max_length=30)
	bsw = models.TextField()

class Video(models.Model):
	 capa = models.ImageField(blank=True)

class Glossario(models.Model):
	nome = models.CharField(max_length=100)
	responsavel = models.ForeignKey(User)

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
	sinalLibras = models.ForeignKey(Video, related_name="sinal")
	descLibras = models.ForeignKey(Video, related_name="descricao")
	exemploLibras = models.ForeignKey(Video, related_name="exemplo")
	variacaoLibras = models.ForeignKey(Video, related_name="variacao")