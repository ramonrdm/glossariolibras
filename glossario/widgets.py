from __future__ import unicode_literals
from django import forms
from django.utils.safestring import mark_safe
from django.template import loader
from glossario.models import CM, Movimentacao, Localizacao
import json

class ImageSelectLocalizacao(forms.Widget):
    template_name = 'widget_localizacao.html'

    class Media:
        css = {'all': ('/static/widgetSelectLocalizacao/widget_localizacao.css', )}
        js = ('/static/widgetSelectLocalizacao/widget_localizacao.js', 'js/jquery.imagemapster.js',)
    
    localizacoes = Localizacao.localizacoes_imagens
    
    def render(self, name, value, attrs=None, renderer=None):
        localizacoes = json.dumps(self.localizacoes)
        template = loader.get_template(self.template_name).render({'objetos': localizacoes,'name': name,'value': value})
        print("localizacoes ------------------>")
        print(value)
        return mark_safe(template)

class ImageSelectMao(forms.Widget):
    template_name = 'widget_mao.html'

    class Media:
        js = ('/static/widgetSelectMao/modalCM.js',)

    def render(self, name, value, attrs=None, renderer=None):
        cm = CM.objects.all()
        cmGrupos = [c.group for c in cm]
        cmGrupos = sorted(list(dict.fromkeys(cmGrupos)))
        template = loader.get_template(self.template_name).render({'objetos': {'nada':'',},'cm': cm, 'cmGrupos': cmGrupos,'name': name,'value': value})
        print("CMs ------------------>")
        print(cmGrupos)
        print(value)
        return mark_safe(template)

class ImageSelectMovimentacao(forms.Widget):
    template_name = 'widget_movimentacao.html'

    class Media:
        js = ('/static/widgetSelectMovimentacao/modalMovimentacao.js',)
        css = {'all': ('/static/widgetSelectMovimentacao/css_movimentacao.css',)}

    def render(self, name, value, attrs=None, renderer=None):
        movimentacao = Movimentacao.movimentacoes_busca
        template = loader.get_template(self.template_name).render({'objetos': {'nada': '',},'movimentacao': movimentacao,'name': name,'value': value})
        print("Movimentacao ------------------>")
        print(value)
        return mark_safe(template)

