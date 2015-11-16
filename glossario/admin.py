# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *
from glossario.forms import GlossarioForm
from unicodedata import normalize 
	
admin.site.register(Localizacao)
admin.site.register(Sinal)

class GlossarioAdmin(admin.ModelAdmin):

	form = GlossarioForm

	def save_model(self, request, obj, form, change):
		gLink = obj.nome.lower()
		gLink = gLink.replace(" ", "-")
		gLink = gLink.encode("utf-8")
		gLink = normalize('NFKD', gLink.decode("utf-8")).encode('ASCII','ignore') 
		obj.link = gLink
		obj.save()



admin.site.register(Glossario, GlossarioAdmin)
	
