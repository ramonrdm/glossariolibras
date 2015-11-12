from django.contrib import admin
from .models import *
from glossario.forms import GlossarioForm
	
admin.site.register(Localizacao)
admin.site.register(Sinal)

class GlossarioAdmin(admin.ModelAdmin):

	form = GlossarioForm
	#def get_form(self, request, obj=None, **kwargs):
	#	self.exclude.append('dataCriacao', 'link')
admin.site.register(Glossario, GlossarioAdmin)