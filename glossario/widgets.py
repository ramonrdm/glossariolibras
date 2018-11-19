from __future__ import unicode_literals
from django.forms.widgets import Select
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.conf import settings

class ImageSelectLocalizacao(Select):

    def __init__(self, attrs=None, choices=(), field_img=None):
        super(ImageSelectLocalizacao, self).__init__(attrs)
        self.choices = list(choices)
        self.field_img = field_img

    localizacoes = dict([('1', 'localizacaoCabeca.png'), ('2', 'localizacaoOmbros.png'), ('3', 'localizacaoBracos.png'),
                         ('4', 'localizacaoNariz.png'), ('5', 'localizacaoBochechas.png'), ('6', 'localizacaoBoca.png'),
                         ('7', 'localizacaoTronco.png'), ('8', 'localizacaoNeutro.png'), ('9', 'localizacaoOlhos.png'),
                         ('10', 'localizacaoOrelhas.png'),
                         ('11', 'localizacaoPescoco.png'), ('12', 'localizacaoQueixo.png'),
                         ('13', 'localizacaoTesta.png')])

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):

        index = str(index) if subindex is None else "%s_%s" % (index, subindex)
        if attrs is None:
            attrs = {}
        option_attrs = self.build_attrs(self.attrs, attrs) if self.option_inherits_attrs else {}
        if selected:
            option_attrs.update(self.checked_attribute)
        if 'id' in option_attrs:
            option_attrs['id'] = self.id_for_label(option_attrs['id'], index)




        if value == '':
            option_attrs['data-img-src'] = '/static/img/X.svg'
        else:
            option_attrs['data-img-src'] = '/static/img/' + self.localizacoes[str(value)]




        return {
            'name': name,
            'value': value,
            'label': label,
            'selected': selected,
            'index': index,
            'attrs': option_attrs,
            'type': self.input_type,
            'template_name': self.option_template_name,
            'wrap_label': True,
        }



class ImageSelectMao(Select):

    def __init__(self, attrs=None, choices=(), field_img=None):
        super(ImageSelectMao, self).__init__(attrs)
        self.choices = list(choices)
        self.field_img = field_img


    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        index = str(index) if subindex is None else "%s_%s" % (index, subindex)
        if attrs is None:
            attrs = {}
        option_attrs = self.build_attrs(self.attrs, attrs) if self.option_inherits_attrs else {}
        if selected:
            option_attrs.update(self.checked_attribute)
        if 'id' in option_attrs:
            option_attrs['id'] = self.id_for_label(option_attrs['id'], index)


        if value == '':
            option_attrs['data-img-src'] = '/static/img/X.svg'
        else:

            option_attrs['data-img-src'] = self.field_img[value - 1]


        return {
            'name': name,
            'value': value,
            'label': label,
            'selected': selected,
            'index': index,
            'attrs': option_attrs,
            'type': self.input_type,
            'template_name': self.option_template_name,
            'wrap_label': True,

        }

