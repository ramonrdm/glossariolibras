# -*- coding: utf-8 -*-

from django import forms
from django.forms.models import ModelChoiceField
from glossario.models import Glossario, Sinal, GrupoCM, CM, UserGlossario
from django.conf import settings
from glossario.widgets import ImageSelectLocalizacao, ImageSelectMao, ImageSelectMovimentacao
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
import re


# --------------------------------------- RegistrationForm ----------------------------------------------------------------

class CustomUserCreationForm(forms.ModelForm):
    email = forms.EmailField(label='Email')
    nome_completo = forms.CharField(label='Nome Completo')
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmar Senha')


    class Meta:
        model = UserGlossario
        fields = ('email',)


    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = UserGlossario.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_nome_completo(self):
        nome_completo = self.cleaned_data['nome_completo']
        return nome_completo

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise ValidationError("Senhas não correspondem")


        minimal_number = 1
        minimal_upper_char = 1
        minimal_lower_char = 1
        minimal_len_char = 8

        if len(password or ()) < minimal_len_char:
            raise forms.ValidationError('Senha tem que ter no mínimo ' + str(minimal_len_char) + ' caracteres')

        if len(re.findall(r"[A-Z]", password)) < minimal_upper_char:
            raise forms.ValidationError('Senha tem que ter no mínimo ' + str(minimal_upper_char) + ' letras maiusculas')

        if len(re.findall(r"[a-z]", password)) < minimal_lower_char:
            raise forms.ValidationError('Senha tem que ter no mínimo ' + str(minimal_lower_char) + ' letras minusculas')

        if len(re.findall(r"[0-9]", password)) < minimal_number:
            raise forms.ValidationError('Senha tem que ter no mínimo ' + str(minimal_number) + ' numeros')

        return password



    def save(self, commit=True):
        user = super().save(commit=False)
        user.nome_completo = self.cleaned_data["nome_completo"]
        user.check_password(self.cleaned_data["password"])
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        return user
#--------------------------------------------------------------------------------------------------------------------------
class GlossarioForm(forms.ModelForm):

	class Meta:
		model = Glossario
		exclude = ['link','dataCriacao']


class SinalForm(forms.ModelForm):
	
	class Meta:
		model = Sinal
		fields = ['glossario', 'traducaoP', 'traducaoI', 'descricao', 'bsw', 'grupoCMe', 'cmE', 'grupoCMd',
		'cmD', 'localizacao', 'movimentacao', 'tema', 'dataPost', 'postador', 'sinalLibras', 'descLibras', 'exemploLibras', 'varicLibras',
		'publicado']
		widgets = {
					'localizacao': ImageSelectLocalizacao(),
					# 'grupoCMe': ImageSelectMao(field_img=('/media/1_xFV5N9L.png', '/media/2_oKcgLJc.png')),
					# 'cmE': ImageSelectMao(),
					# 'grupoCMd': ImageSelectMao(),
					# 'cmD': ImageSelectMao(),
					'movimentacao': ImageSelectMovimentacao()
		}



	def __init__(self, *args, **kwargs):
		super(SinalForm, self).__init__(*args, **kwargs)
		self.fields['bsw'].help_text = "<b><a target='_blank' href='http://glossario.libras.ufsc.br/swis/signmaker.php'>Criar codigo aqui</a></b>"
		self.fields['bsw'].widget = forms.TextInput(attrs={})
		for field in self.fields:
			if field in ['grupoCMd', 'cmD', 'cmE', 'grupoCMe']:
				self.fields[field].widget = ImageSelectMao(choices=self.fields[field].choices, attrs={})
			self.fields[field].widget.field_img = list()
			self.fields[field].empty_label = 'Selecionar'

			for option in range(0, 20):
			# trocar 20 do xrange para length do select que tiver mais options
				if type(self.fields[field]) is ModelChoiceField:
					if len(self.fields[field].queryset) >= option + 1:
						self.fields[field].widget.field_img.append(self.fields[field].queryset[option].imagem.url)
						print(self.fields[field])
						print(self.fields[field].queryset[option].imagem.url)
			print("lista da " + field)
			print(self.fields[field].widget.field_img)


class EnviarSinaisForm(forms.ModelForm):

	class Meta:
		model = Sinal
		fields = ['traducaoP', 'traducaoI', 'descricao', 'localizacao', 'movimentacao', 'grupoCMe', 'cmE', 'grupoCMd', 'cmD',
		'sinalLibras', 'descLibras', 'exemploLibras', 'varicLibras']
		widgets =	{
					'localizacao': ImageSelectLocalizacao(),
					'grupoCMe': ImageSelectMao(),
					'cmE': ImageSelectMao(),
					'grupoCMd': ImageSelectMao(),
					'cmD': ImageSelectMao(),
					'movimentacao': ImageSelectMovimentacao()
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
		fields = ['localizacao', 'grupoCMe', 'cmE', 'movimentacao']
		widgets =	{
					'localizacao': ImageSelectLocalizacao(),
					'grupoCMe': ImageSelectMao(),
					'cmE': ImageSelectMao(),
					'grupoCMd': ImageSelectMao(),
					'cmD': ImageSelectMao(),
					'movimentacao': ImageSelectMovimentacao()
					}


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
						if self.fields[field].queryset[option].imagem:
							self.fields[field].widget.field_img.append(self.fields[field].queryset[option].imagem.url)
						else:
							self.fields[field].widget.field_img.append("/static/img/cinema/")


class GrupoCMForm(forms.ModelForm):

	class Meta:
		model = GrupoCM
		fields = ['imagem', 'bsw']

class CMForm(forms.ModelForm):

	class Meta:
		model = CM
		fields = ['bsw', 'imagem', 'grupo']

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
			self.fields['checkboxPort'].initial = True
			self.fields[field].required = False

#	def clean_nome(self):
#		palavra = self.cleaned_data['nome']
		#tudo para minusculo
		#tirar espacos
		#tirar acentos
		
#		self.exclude.append('link')

#		return self.cleaned_data['nome']