# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import FileField
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.auth import hashers
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
import datetime
import subprocess
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

def profile_upload_path(instance, filename):
	# o arquivo será salvo em MEDIA_ROOT/profile_images/<username>
	return 'profile_images/{0}'.format(instance.user.username)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	lattes = models.CharField('Currículo Lattes', max_length=200, blank=True)
	foto = models.ImageField(upload_to=profile_upload_path, blank=True)

	def __str__(self):
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

	def __str__(self):
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

	def __str__(self):
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
	grupo = models.ForeignKey(GrupoCM, verbose_name = 'Grupo de Configuração de Mão', on_delete=models.CASCADE)

	def image_tag(self):
		if self.imagem:
			return u'<img src="%s" width="50" height="50"/>' % self.imagem.url
		else:
			return 'Sem imagem'
	image_tag.short_description = 'Imagem'
	image_tag.allow_tags = True

	def __str__(self):
		# return str(self.id)+" - "+str(self.grupo)
		return str(self.id)

class Tema(models.Model):
	nome = models.CharField('Nome', max_length=30)
	descricao = models.CharField('Descrição', max_length=100, null=True)
	video = Video('Vídeo', null=True, blank=True)
	imagem = models.ImageField('Imagem', blank=True, null=True)
	temaPai = models.ForeignKey('self',null=True, blank = True, verbose_name = 'Tema Pai', on_delete=models.CASCADE)

	def __str__(self):
		return self.nome

def sinal_upload_path(instance, filename):
	# o arquivo será salvo em MEDIA_ROOT/sinal_videos/originais/<filename>
	return 'sinal_videos/originais/{0}'.format(filename)

class Sinal(models.Model):
	class Meta:
		verbose_name_plural = 'sinais'
		unique_together = ('traducaoP', 'traducaoI', 'grupoCMe', 'cmE', 'grupoCMd', 'cmD', 'localizacao')

	glossario = models.ForeignKey(Glossario, verbose_name='glossário', null=True, on_delete=models.CASCADE)
	traducaoP = models.CharField('palavra', max_length=30)
	traducaoI = models.CharField('word', max_length=30)
	bsw = models.TextField(null=True, blank=True)
	descricao = models.CharField('descrição', max_length=200, null=True)
	grupoCMe = models.ForeignKey(GrupoCM, related_name='Grupo_M_Esquerda', verbose_name='grupo da mão esquerda', on_delete=models.CASCADE)
	cmE = models.ForeignKey(CM, related_name='C_M_Esquerda', verbose_name='configuração da mão esquerda', on_delete=models.CASCADE)
	grupoCMd = models.ForeignKey(GrupoCM, related_name='Grupo_M_Direita', verbose_name='grupo da mão direita', on_delete=models.CASCADE)
	cmD = models.ForeignKey(CM, related_name='C_M_Direita', verbose_name='configuração da mão direita', on_delete=models.CASCADE)
	localizacao = models.ForeignKey(Localizacao, null=True, blank=True, verbose_name='localização', on_delete=models.CASCADE)
	dataPost = models.DateField('data de criação', null=True)
	postador = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	publicado = models.BooleanField(default=False)
	sinalLibras = Video('Vídeo do sinal', upload_to=sinal_upload_path, null=True, blank=True)
	descLibras = Video('Vídeo da descrição', upload_to=sinal_upload_path, null=True, blank=True)
	exemploLibras = Video('Vídeo do exemplo', upload_to=sinal_upload_path, null=True, blank=True)
	varicLibras = Video('Vídeo da variação', upload_to=sinal_upload_path, null=True, blank=True)
	tema = models.ForeignKey(Tema, null=True, on_delete=models.CASCADE)

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

	def __str__(self):
		return self.traducaoP

@receiver(post_save, sender=Sinal)
def update_upload_path(sender, instance, created, **kwargs):
	# o arquivo será salvo em MEDIA_ROOT/sinal_videos/convertidos/<id>-<tag>-<YYYY>-<MM>-<DD>-<HH><MM><SS>

	originais = '{0}/sinal_videos/originais'.format(settings.MEDIA_ROOT)
	convertidos = '{0}/sinal_videos/convertidos'.format(settings.MEDIA_ROOT)

	videoFields = [instance.sinalLibras, instance.descLibras, instance.exemploLibras, instance.varicLibras]
	tags = ['sinal', 'descricao', 'exemplo', 'variacao']

	for index, field in enumerate(videoFields):
		if field:
			subprocess.call('ffmpeg -i {0}/{1} -c:v libx264 -crf 19 -movflags faststart -threads 0 -preset slow -c:a aac -strict -2 {2}/{3}-{4}-%s.mp4'
				.format(
					originais,
					str(field).split('/')[2],
					convertidos,
					instance.id,
					tags[index]
					)
					% datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
					shell=True
					)




from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin