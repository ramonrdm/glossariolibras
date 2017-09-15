# -*- coding: utf-8 -*-
from django.forms.models import ModelChoiceField
from glossario.models import Glossario, Sinal, GrupoCM, CM, Localizacao
from django.conf import settings
from glossario.widgets import ImageSelect
from django import forms

class GlossarioForm(forms.ModelForm):

	class Meta:
		model = Glossario
		exclude = ['link','dataCriacao']

class SinalForm(forms.ModelForm):
	
	class Meta:
		model = Sinal
		fields = ['tema', 'glossario', 'traducaoP', 'traducaoI', 'descricao', 'bsw', 'grupoCMe', 'cmE', 'grupoCMd',
		'cmD', 'localizacao', 'dataPost', 'postador', 'sinalLibras', 'descLibras', 'exemploLibras', 'varicLibras',
		'publicado']

class EnviarSinaisForm(forms.ModelForm):

	class Meta:
		model = Sinal
		fields = ['traducaoP', 'traducaoI', 'descricao', 'localizacao', 'grupoCMe', 'cmE', 'grupoCMd', 'cmD',
		'sinalLibras', 'descLibras', 'exemploLibras', 'varicLibras']
		widgets =	{
					'localizacao': ImageSelect(),
					'grupoCMe': ImageSelect(),
					'cmE': ImageSelect(),
					'grupoCMd': ImageSelect(),
					'cmD': ImageSelect()
					}

	def __init__(self, *args, **kwargs):
		super(EnviarSinaisForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.field_img = list()
			self.fields[field].empty_label = 'Selecionar'
			for option in xrange(0, 20):
			# trocar 20 do xrange para length do select que tiver mais options
				if type(self.fields[field]) is ModelChoiceField:
					if len(self.fields[field].queryset) >= option + 1:
						self.fields[field].widget.field_img.append(self.fields[field].queryset[option].imagem.url)

class PesquisaSinaisForm(forms.ModelForm):

	class Meta:
		model = Sinal
		fields = ['localizacao', 'grupoCMe', 'cmE']
		 # 'grupoCMd', 'cmD'
		widgets =	{
					'localizacao': ImageSelect(),
					'grupoCMe': ImageSelect(),
					'cmE': ImageSelect()
					}
					# 'grupoCMd': ImageSelect(),
					# 'cmD': ImageSelect()

	def __init__(self, *args, **kwargs):
		super(PesquisaSinaisForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.field_img = list()
			self.fields[field].empty_label = 'Selecionar'
			self.fields[field].required = False
			for option in xrange(0, 20):
			# trocar 20 do xrange para length do select que tiver mais options
				if type(self.fields[field]) is ModelChoiceField:
					if len(self.fields[field].queryset) >= option + 1:
						self.fields[field].widget.field_img.append(self.fields[field].queryset[option].imagem.url)

class GrupoCMForm(forms.ModelForm):

	class Meta:
		model = GrupoCM
		fields = ['imagem', 'bsw']

class CMForm(forms.ModelForm):

	class Meta:
		model = CM
		fields = ['bsw', 'imagem', 'grupo']

class LocalizacaoForm(forms.ModelForm):

	class Meta:
		model = Localizacao
		fields = ['nome', 'imagem', 'bsw', 'areaClicavel']

class PesquisaForm(forms.Form):
	busca = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={'id': 'search', 'type': 'search'}))

class PesquisaCheckboxForm(forms.Form):
	checkboxPort = forms.BooleanField(label='Português', widget=forms.CheckboxInput(attrs={
		'type': 'checkbox', 'class': 'filled-in checkboxAzul',
		'id': 'checkboxPort', 'name': 'checkboxPort',
	}))
	checkboxIng = forms.BooleanField(label='Inglês', widget=forms.CheckboxInput(attrs={
		'type': 'checkbox', 'class': 'filled-in checkboxAzul',
		'id': 'checkboxIng', 'name': 'checkboxIng',
	}))

	def __init__(self, *args, **kwargs):
		super(PesquisaCheckboxForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].required = False

#	def clean_nome(self):
#		palavra = self.cleaned_data['nome']
		#tudo para minusculo
		#tirar espacos
		#tirar acentos
		
#		self.exclude.append('link')

#		return self.cleaned_data['nome']