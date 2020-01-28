# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import ModelChoiceField
from glossario.models import Glossario, Sinal, CM, UserGlossario
from django.conf import settings
from glossario.widgets import ImageSelectLocalizacao, ImageSelectMao, ImageSelectMovimentacao
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django_registration.forms import RegistrationForm

class GlossarioForm(forms.ModelForm):
    class Meta:
        model = Glossario
        exclude = ['link','data_criacao']

class SinalForm(forms.ModelForm):

    class Media:
        css = {'all': ('/static/css/materialize_modal.css',)}


    class Meta:
        model = Sinal
        fields = ['glossario', 'portugues', 'ingles', 'descricao', 'bsw', 'cmE',
        'cmD', 'localizacao', 'movimentacao', 'postador', 'video_sinal', 'video_descricao', 'video_exemplo', 'video_variacao',
        'publicado']
        widgets = {
                    'localizacao': ImageSelectLocalizacao(),
                    'cmE': ImageSelectMao(),
                    'cmD': ImageSelectMao(),
                    'movimentacao': ImageSelectMovimentacao()
        }




    def __init__(self, *args, **kwargs):
        super(SinalForm, self).__init__(*args, **kwargs)
        self.fields['bsw'].help_text = "<b><a target='_blank' href='http://glossario.libras.ufsc.br/swis/signmaker.php'>Criar codigo aqui</a></b>"
        self.fields['bsw'].widget = forms.TextInput(attrs={})

class PesquisaSinaisForm(forms.ModelForm):
    class Meta:
        model = Sinal
        fields = ['localizacao', 'cmE', 'movimentacao', ]

        widgets ={
                'localizacao': ImageSelectLocalizacao(),
                'cmE': ImageSelectMao(),
                'movimentacao': ImageSelectMovimentacao()
                 }

    def __init__(self, *args, **kwargs):
        super(PesquisaSinaisForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False


class CMForm(forms.ModelForm):
    class Meta:
        model = CM
        fields = ['bsw', 'name', 'group']

class PesquisaForm(forms.Form):
    busca = forms.CharField(required=False, label="",  widget=forms.TextInput(attrs={'id': 'search', 'type': 'search', 'placeholder': 'Pesquisar em glossário'}))

class CustomRegistrationForm(RegistrationForm):
    class Meta:
        model = UserGlossario
        fields = ['email', 'nome_completo', 'password1', 'password2']