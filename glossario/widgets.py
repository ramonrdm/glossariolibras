from __future__ import unicode_literals
from django.forms.widgets import Select
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils.html import format_html

class ImageSelect(Select):

    class Media:
        css = {
            'all': ('/static/css/image-picker.css',)
        }
        js = ('/static/js/image-picker.js',)

    def __init__(self, attrs=None, choices=(), field_img=None):
        super(ImageSelect, self).__init__(attrs)
        i = -1;
        self.choices = list(choices)
        self.field_img = field_img

    def render_option(self, selected_choices, option_value, option_label):
        i += 1;
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''

        # print 'aquiaquiaquiaquiaquiaquiaquiaqui'
        # print option_value

        # th = None
        # if self.field_img:
        #     if option_value:
        #         rdm = int(option_value) - 2
        #         if 0 < rdm <13:
        #             th = self.field_img[rdm]
        #         else:
        #             th = None

        # if option_value == '':
        #     lista = ''
        # else:
        #     lista = self.field_img[option_value - 1]

        return format_html('<option data-img-src="{}" value="{}"{}>{}</option>',
            self.field_img[i],
            option_value,
            selected_html,
            force_text(option_label)
            )