from django.db import models

# Create your models here.

class Glossario(models.Model):
	nome = models.CharField(max_lengt=100)



class Sinal(models.Model):
	# id

