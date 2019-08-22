from __future__ import unicode_literals
from django.forms.widgets import Select
from django import forms
from django.utils.safestring import mark_safe

from django.template import loader
from django.utils.safestring import mark_safe

from glossario.models import CM


from django.utils.encoding import force_text
from django.utils.html import format_html
from django.conf import settings
from django.template.loader import render_to_string

class ImageSelectLocalizacao(forms.Widget):
    template_name = 'widget_localizacao.html'

    class Media:
        css = {'all': ('/static/widgetSelectLocalizacao/widget_localizacao.css',)}
        js = ('/static/widgetSelectLocalizacao/widget_localizacao.js', )
    
    # def __init__(self, attrs=None, choices=(), field_img=None):
    #     super(ImageSelectLocalizacao, self).__init__(attrs)
    #     self.choices = list(choices)
    #     self.field_img = field_img
    
    localizacoes = dict([('0', 'X.svg'),('1', 'localizacaoCabeca.png'), ('2', 'localizacaoOmbros.png'), ('3', 'localizacaoBracos.png'),
                         ('4', 'localizacaoNariz.png'), ('5', 'localizacaoBochechas.png'), ('6', 'localizacaoBoca.png'),
                         ('7', 'localizacaoTronco.png'), ('8', 'localizacaoNeutro.png'), ('9', 'localizacaoOlhos.png'),
                         ('10', 'localizacaoOrelhas.png'), ('11', 'localizacaoPescoco.png'), ('12', 'localizacaoQueixo.png'),
                         ('13', 'localizacaoTesta.png')])



class ImageSelectMovimentacao(forms.Widget):
    template_name = 'widget_movimentacao.html'

    class Media:
        css = {
            'all': ('/static/widgetSelectMovimentacao/selectMovimentacao.css',)
        }
        js = ('/static/widgetSelectMovimentacao/selectMovimentacao.js', '/static/js/iscroll.js',
              '/static/widgetSelectMovimentacao/widgetMovimentacao.js',)


class ImageSelectMao(forms.Widget):

    class Media:
        # css = {
        #     'all': ('/static/widgetSelectMao/selectMao.css',)
        # }
        js = ('/static/js/modalCM.js',)

    template_name = 'widget_mao.html'

    def render(self, name, value, attrs=None, renderer=None):
        cm = CM.objects.all()
        cmGrupos = [c.group for c in cm]
        cmGrupos = list(dict.fromkeys(cmGrupos))
        template = loader.get_template(self.template_name).render({'cm' : cm, 'cmGrupos' : cmGrupos,})
        return mark_safe(template)




