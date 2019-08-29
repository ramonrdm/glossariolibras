from __future__ import unicode_literals
from django.forms.widgets import Select
from django import forms
from django.utils.safestring import mark_safe
from django.template import loader
from glossario.models import CM, Movimentacao
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.conf import settings
from django.template.loader import render_to_string
import json

class ImageSelectLocalizacao(forms.Widget):
    template_name = 'widget_localizacao.html'

    class Media:
        css = {'all': ('/static/widgetSelectLocalizacao/widget_localizacao.css',)}
        js = ('js/jquery.imagemapster.js', '/static/widgetSelectLocalizacao/widget_localizacao.js', )
    
    # def __init__(self, attrs=None, choices=(), field_img=None):
    #     super(ImageSelectLocalizacao, self).__init__(attrs)
    #     self.choices = list(choices)
    #     self.field_img = field_img
    
    localizacoes = dict([('0', 'X.svg'),('1', 'localizacaoCabeca.png'), ('2', 'localizacaoOmbros.png'), ('3', 'localizacaoBracos.png'),
                         ('4', 'localizacaoNariz.png'), ('5', 'localizacaoBochechas.png'), ('6', 'localizacaoBoca.png'),
                         ('7', 'localizacaoTronco.png'), ('8', 'localizacaoNeutro.png'), ('9', 'localizacaoOlhos.png'),
                         ('10', 'localizacaoOrelhas.png'), ('11', 'localizacaoPescoco.png'), ('12', 'localizacaoQueixo.png'),
                         ('13', 'localizacaoTesta.png')])
    
    def render(self, name, value, attrs=None, renderer=None):
        loc = json.dumps(self.localizacoes)
        template = loader.get_template(self.template_name).render({'localizacoes': loc,})
        return mark_safe(template)

class ImageSelectMovimentacao(forms.Widget):
    template_name = 'widget_movimentacao.html'

    class Media:
        js = ('/static/widgetSelectMovimentacao/modalMovimentacao.js',)

    def render(self, name, value, attrs=None, renderer=None):
        movimentacao = Movimentacao.movimentacoes_imagens
        template = loader.get_template(self.template_name).render({'movimentacao': movimentacao,})
        return mark_safe(template)

class ImageSelectMao(forms.Widget):
    template_name = 'widget_mao.html'

    class Media:
        js = ('/static/widgetSelectMao/modalCM.js',)

    def render(self, name, value, attrs=None, renderer=None):
        cm = CM.objects.all()
        cmGrupos = [c.group for c in cm]
        cmGrupos = sorted(list(dict.fromkeys(cmGrupos)))
        template = loader.get_template(self.template_name).render({'cm': cm, 'cmGrupos': cmGrupos, })
        return mark_safe(template)



