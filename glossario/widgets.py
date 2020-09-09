from __future__ import unicode_literals
import json
from django import forms
from django.utils.safestring import mark_safe
from django.template import loader
from django.forms.widgets import ClearableFileInput
from glossario.models import CM, Movimentacao, Localizacao

class ImageSelectLocalizacao(forms.Widget):
    template_name = 'glossario/widget_localizacao.html'

    class Media:
        css = {'all': ('/static/widgetSelectLocalizacao/widget_localizacao.css', )}
        js = ('/static/widgetSelectLocalizacao/widget_localizacao.js', 'js/jquery.imagemapster.js',)
    
    
    def render(self, name, value, attrs=None, renderer=None):
        local_nomes = dict(Localizacao.localizacoes)
        localizacoes = Localizacao.localizacoes_imagens
        template = loader.get_template(self.template_name).render({'objetos': localizacoes,'local_nomes': local_nomes, 'name': name,'value': value})

        return mark_safe(template)

class ImageSelectMao(forms.Widget):
    template_name = 'glossario/widget_mao.html'

    def render(self, name, value, attrs=None, renderer=None):
        cm = CM.objects.all()
        cmGrupos = [c.group for c in cm]
        cmGrupos = sorted(list(dict.fromkeys(cmGrupos)))
        template = loader.get_template(self.template_name).render({'objetos': {'nada':'',},'cm': cm, 'cmGrupos': cmGrupos,'name': name,'value': value})

        return mark_safe(template)

class ImageSelectMovimentacao(forms.Widget):
    template_name = 'glossario/widget_movimentacao.html'

    class Media:
        css = {'all': ('/static/widgetSelectMovimentacao/css_movimentacao.css',)}

    def render(self, name, value, attrs=None, renderer=None):
        movimentacao = Movimentacao.movimentacoes_imagens.values()
        template = loader.get_template(self.template_name).render({'objetos': {'nada': '',},'movimentacao': movimentacao,'name': name,'value': value})

        return mark_safe(template)

class VideoInput(ClearableFileInput):
    template_name = 'admin/video_clearable_file_input.html'