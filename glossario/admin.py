# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *
from glossario.forms import GlossarioForm, SinalForm
from unicodedata import normalize 

admin.site.register(Usuario)
admin.site.register(Localizacao)
admin.site.register(GrupoCM)
admin.site.register(CM)
admin.site.register(Tema)

#

class GlossarioAdmin(admin.ModelAdmin):

	form = GlossarioForm

	def save_model(self, request, obj, form, change):
		gLink = obj.nome.lower()
		gLink = gLink.replace(" ", "-")
		gLink = gLink.encode("utf-8")
		gLink = normalize('NFKD', gLink.decode("utf-8")).encode('ASCII','ignore') 
		obj.link = gLink
		obj.save()	

class SinalAdmin(admin.ModelAdmin):

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

admin.site.register(Glossario, GlossarioAdmin)
admin.site.register(Sinal, SinalAdmin)
