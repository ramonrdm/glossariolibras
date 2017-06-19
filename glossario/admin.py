# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *
from glossario.forms import GlossarioForm, SinalForm, UsuarioForm
from unicodedata import normalize
from django.db import models
from django.db.models import Q

admin.site.register(Localizacao)
admin.site.register(GrupoCM)
admin.site.register(CM)
admin.site.register(Tema)

class GlossarioAdmin(admin.ModelAdmin):

    def has_module_permission(self, request):
        return True
        
    def get_queryset(self, request):
        qs = super(GlossarioAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs        
        return qs.filter(responsavel=request.user)

    # def has_add_permission(self, request):
    #     if request.user.is_superuser:
    #     	return True

    # def has_change_permission(self, request, obj=None):
    #     if obj is None:
    #         return False
    #     if request.user.is_superuser or obj.responsavel == request.user:
    #     	return True
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     if obj is None:
    #         return False
    #     # if obj.responsavel == request.user:
    #     #     return True
    #     if request.user.is_superuser:
    #     	return True
    #     return False


	form = GlossarioForm

	def save_model(self, request, obj, form, change):
		gLink = obj.nome.lower()
		gLink = gLink.replace(" ", "-")
		gLink = gLink.encode("utf-8")
		gLink = normalize('NFKD', gLink.decode("utf-8")).encode('ASCII','ignore') 
		obj.link = gLink
		obj.save()	

class SinalAdmin(admin.ModelAdmin):

	def get_queryset(self, request):
		qs = super(SinalAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		# qsResponsavel = qs.filter(glossario__responsavel=request.user)
		# if glossario__membros__icontains(request.user):
		# 	qsMembro = qs.filter(glossario__membros=request.user)
		# 	qsMembro.readonly_fields = '__all__'
		# return qsResponsavel, qsMembro
		return qs.filter(Q(glossario__responsavel=request.user) | Q(glossario__membros=request.user))

	form = SinalForm

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
