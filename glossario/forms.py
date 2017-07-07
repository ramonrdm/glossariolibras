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

	# grupoCMe = ForeignKey(
	# 	GrupoCM,
	# 	related_name='Grupo_M_Esquerda',
	# 	verbose_name='grupo de configuração de mão esquerda',
	# 	attrs={'data-icon': {{grupoCMe.imagem.url}}}
	# 	)

	class Meta:
		model = Sinal
		fields = ['traducaoP', 'traducaoI', 'descricao', 'grupoCMe', 'cmE', 'grupoCMd', 'cmD', 'localizacao',
		'sinalLibras', 'descLibras', 'exemploLibras', 'varicLibras']
		# widgets = {
		# 'grupoCMe': forms.Select(attrs={'data-icon': '{{grupoCMe.imagem.url}}'}),
		# }

	def __init__(self, *args, **kwargs):
		super(EnviarSinaisForm, self).__init__(*args, **kwargs)
		self.fields['grupoCMe'].empty_label = 'Selecione um grupo'
		# self.fields['grupoCMe'].widget.attrs['class'] = '{{grupoCMe.imagem.url}}'
		self.fields['grupoCMd'].empty_label = 'Selecione um grupo'
		self.fields['cmE'].empty_label = 'Selecione uma configuração'
		self.fields['cmD'].empty_label = 'Selecione um configuração'
		self.fields['localizacao'].empty_label = 'Selecione uma localização'

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

#	def clean_nome(self):
#		palavra = self.cleaned_data['nome']
		#tudo para minusculo
		#tirar espacos
		#tirar acentos
		
#		self.exclude.append('link')

#		return self.cleaned_data['nome']