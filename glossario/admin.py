# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *
from glossario.forms import GlossarioForm
from unicodedata import normalize 
	
admin.site.register(Localizacao)
admin.site.register(Sinal)

class GlossarioAdmin(admin.ModelAdmin):

	form = GlossarioForm
	#def get_form(self, request, obj=None, **kwargs):
	#	self.exclude.append('dataCriacao', 'link')
	def save_model(self, request, obj, form, change):
		gLink = obj.nome.lower()
		gLink = gLink.replace(" ", "-")
		gLink = unicode(gLink)
		gLink = normalize('NFKD', gLink.encode('ASCII','ignore'))
		
		print "AQUIIIIIIIIIIIIII   >>>>"
		print gLink
		obj.link = gLink
		obj.save()



admin.site.register(Glossario, GlossarioAdmin)
	
