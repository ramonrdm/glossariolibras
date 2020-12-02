# -*- coding: utf-8 -*-
from django import forms
from glossario.models import Glossario, Sinal, CM, UserGlossario, Area, Comment
from glossario.widgets import VideoInput, ImageSelectLocalizacao, ImageSelectMao, ImageSelectMovimentacao
from django_registration.forms import RegistrationForm


class GlossarioForm(forms.ModelForm):
    class Meta:
        model = Glossario
        exclude = ['link', 'data_criacao']

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nome', 'parent']
        exclude = ['slug']

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
            'movimentacao': ImageSelectMovimentacao(),
            'video_sinal': VideoInput(),
            'video_descricao': VideoInput(),
            'video_exemplo': VideoInput(),
            'video_variacao': VideoInput(),
        }

    def __init__(self, *args, **kwargs):
        super(SinalForm, self).__init__(*args, **kwargs)
        self.fields['bsw'].help_text = "<b><a target='_blank' href='http://glossario.libras.ufsc.br/swis/signmaker.php'>Criar codigo aqui</a></b>"
        self.fields['bsw'].widget = forms.TextInput(attrs={})
    
    def clean(self):
        cleaned_data = super().clean()
        publicado = cleaned_data.get("publicado")
        if publicado:
            movimento = cleaned_data.get("movimentacao")
            localizacao = cleaned_data.get("localizacao")
            cm_esq = cleaned_data.get("cmE")
            cm_dir = cleaned_data.get("cmD")
            if movimento is None:
                self._errors['movimentacao'] = self.error_class([
                    "Movimento deve ser selecionado"
                ])

            if localizacao is None:
                self._errors['localizacao'] = self.error_class([
                    "Localizacao deve ser selecionado"
                ])

            if cm_esq is None:
                self._errors['cmE'] = self.error_class([
                    "Algum movimento deve ser selecionado"
                ])

            if cm_dir is None:
                self._errors['cmD'] = self.error_class([
                    "Algum movimento deve ser selecionado"
                ])
        return self.cleaned_data


class PesquisaSinaisForm(forms.ModelForm):
    class Meta:
        model = Sinal
        fields = ['localizacao', 'cmE', 'movimentacao']
        widgets = {
            'localizacao': ImageSelectLocalizacao(),
            'cmE': ImageSelectMao(),
            'movimentacao': ImageSelectMovimentacao()
        }

    busca = forms.CharField(required=False, label="",  widget=forms.TextInput(
        attrs={'id': 'search', 'type': 'search', 'placeholder': 'Pesquisar em glossário'}))
    areas = forms.ModelMultipleChoiceField(queryset=Area.objects.all())
    glossarios = forms.ModelMultipleChoiceField(queryset=Glossario.objects.all())
    letra_inicial = forms.CharField(max_length=1, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(PesquisaSinaisForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False


class CMForm(forms.ModelForm):
    class Meta:
        model = CM
        fields = ['bsw', 'name', 'group']


class CustomRegistrationForm(RegistrationForm):
    class Meta:
        model = UserGlossario
        fields = ['email', 'nome_completo', 'password1', 'password2']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comentario']