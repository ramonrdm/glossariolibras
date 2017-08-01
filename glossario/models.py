# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import FileField
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.auth import hashers
from django.db.models import F
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
import datetime
import subprocess

def profile_upload_path(instance, filename):
	# o arquivo será salvo em MEDIA_ROOT/profile_images/user_<id>/<filename>
	return 'profile_images/{0}'.format(instance.user.username)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	lattes = models.CharField('Currículo Lattes', max_length=200, blank=True)
	foto = models.ImageField(upload_to=profile_upload_path, blank=True)

	def __unicode__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
	instance.profile.save()

class Localizacao(models.Model):
	class Meta:
		verbose_name_plural='localizações'

	nome = models.CharField('Nome', max_length=30)
	bsw = models.TextField('BSW')
	imagem = models.ImageField('Imagem', blank=True)
	areaClicavel = models.TextField()

	def image_tag(self):
		if self.imagem:
			return u'<img src="%s" width="50" height="50"/>' % self.imagem.url
		else:
			return 'Sem imagem'
	image_tag.short_description = 'Imagem'
	image_tag.allow_tags = True

	def __unicode__(self):
		return self.nome

class Video(FileField):
	capa = models.ImageField(blank=True)
	videoMp4 = models.FileField()

class Glossario(models.Model):
	class Meta:
		verbose_name='glossário'

	nome = models.CharField('Nome do Glossário', max_length=100)
	responsavel = models.ManyToManyField(User, verbose_name = 'responsável')
	membros = models.ManyToManyField(User, related_name='glossario_membros', verbose_name='membros', blank=True)
	descricao = models.TextField("descrição", default='')
	imagem = models.ImageField('Imagem', blank=True)
	link = models.CharField('Link', max_length=20)
	dataCriacao = models.DateField('data de criação', auto_now_add=True)
	videoGlossario = Video('Vídeo', blank=True)

	def image_tag(self):
		if self.imagem:
			return u'<img src="%s" width="50" height="50"/>' % self.imagem.url
		else:
			return 'Sem imagem'
	image_tag.short_description = 'Imagem'
	image_tag.allow_tags = True

	def __unicode__(self):
		return self.nome

class GrupoCM (models.Model):
	class Meta:
		verbose_name_plural='Grupos de configuração de mão'

	imagem = models.ImageField(blank=True)
	bsw = models.TextField('BSW')

	def image_tag(self):
		if self.imagem:
			return u'<img src="%s" width="50" height="50"/>' % self.imagem.url
		else:
			return 'Sem imagem'
	image_tag.short_description = 'Imagem'
	image_tag.allow_tags = True

	def __str__(self):
		return str(self.id)

class CM (models.Model):
	class Meta:
		verbose_name_plural='configurações de mão'

	bsw = models.TextField('BSW', blank=True, default='')
	imagem = models.ImageField(blank=True)
	grupo = models.ForeignKey(GrupoCM, verbose_name = 'Grupo de Configuração de Mão')

	def image_tag(self):
		if self.imagem:
			return u'<img src="%s" width="50" height="50"/>' % self.imagem.url
		else:
			return 'Sem imagem'
	image_tag.short_description = 'Imagem'
	image_tag.allow_tags = True

	def __str__(self):
		return str(self.id)+" - "+str(self.grupo)

class Tema(models.Model):
	nome = models.CharField('Nome', max_length=30)
	descricao = models.CharField('Descrição', max_length=100, null=True)
	video = Video('Vídeo', null=True, blank=True)
	imagem = models.ImageField('Imagem', blank=True, null=True)
	temaPai = models.ForeignKey('self',null=True, blank = True, verbose_name = 'Tema Pai')

	def __unicode__(self):
		return self.nome

def sinal_upload_path(instance, filename):
	return 'sinal_videos/originais/{0}'.format(filename)

	# def switch(instance=None, filename=None, tipo=None):
	# 	return {
	# 		'sinal': 'sinal_videos/%Y/%m/%d/sinal_{0}/sinal_{1}'.format(instance.id, filename),
	# 		'descricao': 'sinal_videos/%Y/%m/%d/sinal_{0}/descricao_{1}'.format(instance.id, filename),
	# 		'exemplo': 'sinal_videos/%Y/%m/%d/sinal_{0}/exemplo_{1}'.format(instance.id, filename),
	# 		'variacao': 'sinal_videos/%Y/%m/%d/sinal_{0}/variacao_{1}'.format(instance.id, filename),
	# 		'padrao': 'sinal_videos/%Y/%m/%d/sinal_{0}/{1}'.format(instance.id, filename)
	# 	}.get(tipo, 'padrao')

	# return switch(tipo)

	# if tipo == 'sinal':
	# 	return 'sinal_videos/%Y/%m/%d/sinal_{0}/{1}'.format(id, tipo)
	# elif tipo == 'descricao':
	# 	return 'sinal_videos/%Y/%m/%d/sinal_{0}/{1}'.format(id, tipo)
	# elif tipo == 'exemplo':
	# 	return 'sinal_videos/%Y/%m/%d/sinal_{0}/{1}'.format(id, tipo)
	# elif tipo == 'variacao':
	# 	return 'sinal_videos/%Y/%m/%d/sinal_{0}/{1}'.format(id, tipo)
	# return 'sinal_videos/%Y/%m/%d/sinal_{0}/'.format(id)

	# return 'sinal_videos/%Y/%m/%d/sinal_{0}/{1}'.format(instance.id, filename)

class Sinal(models.Model):
	class Meta:
		verbose_name_plural='sinais'
		unique_together = ('traducaoP', 'traducaoI', 'grupoCMe', 'cmE', 'grupoCMd', 'cmD', 'localizacao')

	glossario = models.ForeignKey(Glossario, verbose_name='glossário', null=True)
	traducaoP = models.CharField('palavra', max_length=30)
	traducaoI = models.CharField('word', max_length=30)
	bsw = models.TextField(null=True, blank=True)
	descricao = models.CharField('descrição', max_length=200, null=True)
	grupoCMe = models.ForeignKey(GrupoCM, related_name='Grupo_M_Esquerda', verbose_name='grupo da mão esquerda')
	cmE = models.ForeignKey(CM, related_name='C_M_Esquerda', verbose_name='configuração da mão esquerda')
	grupoCMd = models.ForeignKey(GrupoCM, related_name='Grupo_M_Direita', verbose_name='grupo da mão direita')
	cmD = models.ForeignKey(CM, related_name='C_M_Direita', verbose_name='configuração da mão direita')
	localizacao = models.ForeignKey(Localizacao, null=True, blank=True, verbose_name='localização')
	dataPost = models.DateField('data de criação', null=True)
	postador = models.ForeignKey(User, null=True)
	publicado = models.BooleanField(default=False)
	sinalLibras = Video('Vídeo do sinal', upload_to=sinal_upload_path, null=True, blank=True)
	descLibras = Video('Vídeo da descrição', upload_to=sinal_upload_path, null=True, blank=True)
	exemploLibras = Video('Vídeo do exemplo', upload_to=sinal_upload_path, null=True, blank=True)
	varicLibras = Video('Vídeo da variação', upload_to=sinal_upload_path, null=True, blank=True)
	tema = models.ForeignKey(Tema, null=True)

	def image_tag_cmE(self):
		if self.cmE.imagem:
			return u'<img src="%s" width="50" height="50"/>' % self.cmE.imagem.url
		else:
			return 'Sem imagem'
	image_tag_cmE.short_description = 'esquerda'
	image_tag_cmE.allow_tags = True

	def image_tag_cmD(self):
		if self.cmD.imagem:
			return u'<img src="%s" width="50" height="50"/>' % self.cmD.imagem.url
		else:
			return 'Sem imagem'
	image_tag_cmD.short_description = 'direita'
	image_tag_cmD.allow_tags = True

	def image_tag_localizacao(self):
		if self.localizacao:
			if self.localizacao.imagem:
				return u'<img src="%s" width="50" height="50"/>' % self.localizacao.imagem.url
		return 'Sem imagem'

	image_tag_localizacao.short_description = 'localização'
	image_tag_localizacao.allow_tags = True

	def __unicode__(self):
		return self.traducaoP

@receiver(post_save, sender=Sinal)
def update_upload_path(sender, instance, created, **kwargs):

	originais = '{0}/sinal_videos/originais'.format(settings.MEDIA_ROOT)
	convertidos = '{0}/sinal_videos/convertidos'.format(settings.MEDIA_ROOT)

	videoFields = [instance.sinalLibras, instance.descLibras, instance.exemploLibras, instance.varicLibras]
	tags = ['sinal', 'descricao', 'exemplo', 'variacao']

	for index, field in enumerate(videoFields):
		if field:
			subprocess.call('cp {0}/{1} {2}/{3}-{4}-%s'.format(
					originais,
					str(field).split('/')[2],
					convertidos,
					instance.id,
					tags[index]
					)
					% datetime.datetime.now().strftime('%Y-%m-%d-%X'),
					shell=True)