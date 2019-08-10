from __future__ import unicode_literals
from django.forms.widgets import Select
from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.conf import settings
from django.template.loader import render_to_string

class ImageSelectLocalizacao(forms.Widget):
    template_name = 'widget_localizacao.html'

    # class Media:
        
        # css = {
        #     'all': ('/static/image-picker/image-picker/image-picker.css',)
        # }
        # js = ('/static/image-picker/image-picker/image-picker.js', '/static/js/jquery.imagemapster.js', '/static/js/baseSearchNav.js', )


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

    # class Media:
    #     css = {
    #         'all': ('/static/widgetSelectMovimentacao/selectMovimentacao.css',)
    #     }
    #     js = ('/static/widgetSelectMovimentacao/selectMovimentacao.js', '/static/js/iscroll.js',
    #           '/static/widgetSelectMovimentacao/widgetMovimentacao.js',)
    #

class ImageSelectMao(forms.Widget):
    template_name = 'widget_mao.html'

    class Media:
        css = {
            'all': ('/static/widgetSelectMao/selectMao.css',)
        }
        js = ('/static/widgetSelectMao/selectMao.js', '/static/js/iscroll.js', '/static/widgetSelectMao/widgetMao.js',)


