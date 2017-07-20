# -*- coding: utf-8 -*-
from glossario.models import Usuario, Glossario, Sinal, GrupoCM, CM, Localizacao
from django import forms

class UsuarioForm(forms.ModelForm):

	class Meta:
		model = Usuario
		widgets = {
		'password': forms.PasswordInput(),
		}
		fields = ['username', 'password', 'nome', 'latte', 'foto', 'email', 'is_staff', 'groups']
		
	def  save(self, commit=True):
		user = super(UsuarioForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user

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

	def __init__(self, *args, **kwargs):
		super(EnviarSinaisForm, self).__init__(*args, **kwargs)
		for fields in self.fields:
			self.fields[fields].empty_label = 'Selecione um item'

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
		'type': 'checkbox', 'class': 'filled-in ',
		'id': 'checkboxIng', 'name': 'checkboxIng',
	}))

	def __init__(self, *args, **kwargs):
		super(PesquisaCheckboxForm, self).__init__(*args, **kwargs)
		for fields in self.fields:
			self.fields[fields].required = False

class PesquisaCheckboxIngForm(forms.Form):
	checkboxIng = forms.BooleanField(label='Inglês', widget=forms.CheckboxInput(attrs={
		'type': 'checkbox', 'class': 'filled-in checkboxAzul',
		'id': 'checkboxIng', 'name': 'checkboxIng',
	}))

	def __init__(self, *args, **kwargs):
		super(PesquisaCheckboxIngForm, self).__init__(*args, **kwargs)
		for fields in self.fields:
			self.fields[fields].required = False

#	def clean_nome(self):
#		palavra = self.cleaned_data['nome']
		#tudo para minusculo
		#tirar espacos
		#tirar acentos
		
#		self.exclude.append('link')

#		return self.cleaned_data['nome']