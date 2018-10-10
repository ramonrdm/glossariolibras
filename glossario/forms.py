# -*- coding: utf-8 -*-
from django.forms.models import ModelChoiceField
from glossario.models import Glossario, Sinal, GrupoCM, CM, Localizacao, UserGlossario
from django.conf import settings
from glossario.widgets import ImageSelect
from django import forms

# --------------------------------------- RegistrationForm ----------------------------------------------------------------

from django.contrib.auth.forms import UserCreationForm
from glossario.models import UserGlossario
from django.core.exceptions import ValidationError


class CustomUserCreationForm(forms.Form):
    email = forms.EmailField(label='Email')
    # nome_completo = forms.CharField(label="Nome Completo")
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput)



    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = UserGlossario.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    # def clean_nome_completo(self):
    #     nome_completo = self.cleaned_data['nome_completo'].lower()
    #     r = UserGlossario.objects.filter(nome_completo=nome_completo)
    #     if r.count():
    #         raise ValidationError("Username already exists")
    #     return nome_completo

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise ValidationError("Senhas não correspondem")

        return password2

    def save(self, commit=True):
        user = UserGlossario.objects.create_user(
            self.cleaned_data['email'],
            # self.cleaned_data['nome_completo'],
            self.cleaned_data['password']
        )
        return user

#--------------------------------------------------------------------------------------------------------------------------
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
			for option in range(0, 20):
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
			for option in range(0, 20):
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