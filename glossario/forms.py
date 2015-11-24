# -*- coding: utf-8 -*-

from glossario.models import Glossario, Sinal
from django import forms
import datetime

class GlossarioForm(forms.ModelForm):

	class Meta:
		model = Glossario
		exclude = ['link','dataCriacao']

class PesquisaPortForm(forms.Form):

	model = Sinal
	fields = 'traducaoP'
	TraducaoP = forms.CharField(max_length=30)

class PesquisaIngForm(forms.Form):
	model = Sinal
	fields = 'traducaoI'
	TraducaoI = forms.CharField(max_length=30)

#	def clean_nome(self):
#		palavra = self.cleaned_data['nome']
		#tudo para minusculo
		#tirar espacos
		#tirar acentos
		
#		self.exclude.append('link')

#		return self.cleaned_data['nome']