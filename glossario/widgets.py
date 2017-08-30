from __future__ import unicode_literals
from django.forms.widgets import Select
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.conf import settings

class ImageSelect(Select):

    def __init__(self, attrs=None, choices=(), field_img=None):
        super(ImageSelect, self).__init__(attrs)
        self.choices = list(choices)
        self.field_img = field_img

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                selected_choices.remove(option_value)
        else:
            selected_html = ''

        i = img = None
        if option_value != '':
            i = int(option_value) - 1
            img = self.field_img[i]
        else:
            img = '/static/img/X.svg'

        return format_html('<option data-img-src="{}" value="{}"{}>{}</option>',
            img,
            option_value,
            selected_html,
            force_text(option_label)
            )

class MapSelect(Select):

    def __init__(self, attrs=None, choices=(), field_img=None):
        super(MapSelect, self).__init__(attrs)
        self.choices = list(choices)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html('<img id="modeloImg" src="/static/img/modelo.png" alt="" usemap="#modeloMap"{}/><map name="modeloMap" id="modeloMap">', flatatt(final_attrs))]
        options = self.render_options([value])
        if options:
            output.append(options)
        output.append('</map>')
        return mark_safe('\n'.join(output))

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                selected_choices.remove(option_value)
        else:
            selected_html = ''

        if option_value == '':
            option_value = 1

        return format_html('<option value="{}"><area id="id1" data-key="A" alt="" title="" href="#" shape="poly" coords="304,149,274,349,649,360,582,89,417,34,345,42,304"/></option>',
            option_value,
            selected_html,
            force_text(option_label)
            )