# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from glossario.models import Glossario, Sinal, Usuario
from django import forms
import datetime

class CriandoUser(UserCreationForm):
	email = forms.EmailField(required = False)

	class Meta:
	    model = Usuario
	    fields = ('username', 'email', 'foto', 'password1', 'password2','latte')

	def save(self,commit = False):   
	    user = super(CriandoUser, self).save(commit = False)
	    user.email = self.cleaned_data['email']
	    user.user_mobile = self.cleaned_data['latte']
	    user.set_password(self.cleaned_data["password1"])

	    user_default = User.objects.create_user(self.cleaned_data['username'], self.cleaned_data['email'], self.cleaned_data['password1'])
	    user_default.save()

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


class PesquisaIngForm(forms.ModelForm):
	
	class Meta:
		model = Sinal
		fields = ['traducaoI']

class SinalForm(forms.ModelForm):

	class Meta:
		model = Sinal
		fields = '__all__'

#


#	def clean_nome(self):
#		palavra = self.cleaned_data['nome']
		#tudo para minusculo
		#tirar espacos
		#tirar acentos
		
#		self.exclude.append('link')

#		return self.cleaned_data['nome']