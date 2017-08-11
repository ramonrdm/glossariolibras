# -*- coding: utf-8 -*-
from glossario.models import Glossario, Sinal, GrupoCM, CM, Localizacao
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
					'localizacao': ImageSelect(attrs={'class': 'image-picker'}),
					'grupoCMe': ImageSelect(attrs={'class': 'image-picker'}),
					'cmE': ImageSelect(attrs={'class': 'image-picker'}),
					'grupoCMd': ImageSelect(attrs={'class': 'image-picker'}),
					'cmD': ImageSelect(attrs={'class': 'image-picker'})
					}

	def __init__(self, *args, **kwargs):
		super(EnviarSinaisForm, self).__init__(*args, **kwargs)
		i = 0
		self.fields['localizacao'].widget.field_img = list()
		for field in self.fields:
			self.fields[field].empty_label = 'Selecione um item'
			self.fields['localizacao'].widget.field_img.append(self.fields['localizacao'].queryset[i].imagem.url)
			i = i + 1

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
	busca = forms.CharField(label="", widget=forms.TextInput(attrs={'id': 'search', 'type': 'search'}))

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