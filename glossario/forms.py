# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from glossario.models import Glossario, Sinal, Usuario
from django import forms
import datetime


class UsuarioForm(forms.ModelForm):

	class Meta:
		model = Usuario
		widgets = {
		'password': forms.PasswordInput(),
		}
		fields = ['username', 'password', 'nome', 'latte', 'foto', 'email']
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

class PesquisaPortForm(forms.ModelForm):
	
	class Meta:
		model = Sinal
		fields = ['traducaoP']
		widgets = {
        	'traducaoP': forms.TextInput(attrs={'id': 'search', 'type': 'search'}),
        }

class PesquisaIngForm(forms.ModelForm):
	
	class Meta:
		model = Sinal
		fields = ['traducaoI']

class SinalForm(forms.ModelForm):

	class Meta:
		model = Sinal
		fields = '__all__'

class PesquisaForm(forms.Form):
	busca = forms.CharField(label="", widget=forms.TextInput(attrs={'id': 'search', 'type': 'search'}))
#


#	def clean_nome(self):
#		palavra = self.cleaned_data['nome']
		#tudo para minusculo
		#tirar espacos
		#tirar acentos
		
#		self.exclude.append('link')

#		return self.cleaned_data['nome']