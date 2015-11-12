# -*- coding: utf-8 -*-

from glossario.models import Glossario
from django import forms
import datetime

class GlossarioForm(forms.ModelForm):

	class Meta:
		model = Glossario
		exclude = ['link', 'dataCriacao']

	def clean_nome(self):
		palavra = self.cleaned_data['nome']
		#tudo para minusculo
		#tirar espacos
		#tirar acentos
		self.fields['link'] = palavra

		return self.cleaned_data['nome']