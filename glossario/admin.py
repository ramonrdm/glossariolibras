# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *
from glossario.forms import GlossarioForm, SinalForm, UsuarioForm
from unicodedata import normalize
from django.db import models
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType

admin.site.register(Localizacao)
admin.site.register(GrupoCM)
admin.site.register(CM)
admin.site.register(Tema)

class GlossarioAdmin(admin.ModelAdmin):
	
	form = GlossarioForm
	list_filter = ('responsavel', 'membros', 'dataCriacao')

	def get_readonly_fields(self, request, obj=None):
		qs = super(GlossarioAdmin, self).get_queryset(request)
		qsResp = qs.filter(responsavel=request.user)
		qsMemb = qs.filter(membros=request.user)
		if obj in qsResp or request.user.is_superuser:
			return []
		if obj in qsMemb:
			return ('nome', 'responsavel', 'membros', 'imagem', 'videoGlossario')
		return []

	def get_actions(self, request):
		actions = super(GlossarioAdmin, self).get_actions(request)
		if not request.user.is_superuser:
			if 'delete_selected' in actions:
				del actions['delete_selected']
		return actions

	def get_queryset(self, request):
		qs = super(GlossarioAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(Q(responsavel=request.user) | Q(membros=request.user))

	def has_add_permission(self, request):
		if request.user.is_superuser:
			return True
		return False

	def save_model(self, request, obj, form, change):
		gLink = obj.nome.lower()
		gLink = gLink.replace(" ", "-")
		gLink = gLink.encode("utf-8")
		gLink = normalize('NFKD', gLink.decode("utf-8")).encode('ASCII','ignore') 
		obj.link = gLink
		obj.save()	

class SinalAdmin(admin.ModelAdmin):

	form = SinalForm
	list_filter = ('tema', 'glossario', 'localizacao', 'dataPost', 'publicado')

	def get_queryset(self, request):
		qs = super(SinalAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(Q(glossario__responsavel=request.user) | Q(glossario__membros=request.user))

	def get_readonly_fields(self, request, obj=None):
		qs = super(SinalAdmin, self).get_queryset(request)
		qsResp = qs.filter(glossario__responsavel=request.user)
		qsMemb = qs.filter(glossario__membros=request.user)
		if obj in qsResp or request.user.is_superuser:
			return []
		if obj in qsMemb:
			# return self.fields or [f.name for f in self.model._meta.fields]
			return ('glossario', 'traducaoP', 'traducaoI', 'bsw', 'descricao', 'grupoCMe', 'cmE',
				'grupoCMd', 'cmD', 'localizacao', 'sinalLibras', 'descLibras', 'varicLibras',
				'exemploLibras', 'tema',
			)
		return []

	def save_model(self, request, obj, form, change):
		obj.dataPost = datetime.date.today()
		obj.postador = request.user
		obj.save()

	def get_form(self, request, obj, **kwargs):
		self.exclude = ['postador','dataPost']
		responsaveis = Glossario.objects.filter(responsavel=request.user)
		if not request.user.is_superuser or responsaveis:
			self.exclude.append('publicado')
		return super(SinalAdmin, self).get_form(request, obj, **kwargs)

class UsuarioAdmin(admin.ModelAdmin):

	form = UsuarioForm



admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Glossario, GlossarioAdmin)
admin.site.register(Sinal, SinalAdmin)