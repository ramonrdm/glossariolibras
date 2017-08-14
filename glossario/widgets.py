from __future__ import unicode_literals
from django.forms.widgets import Select
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.conf import settings

class ImageSelect(Select):

    # class Media:
    #     cssPath = '{0}/css/image-picker.css'.format(settings.STATIC_ROOT)
    #     cssPath2 = '{0}/css/image-picker.scss'.format(settings.STATIC_ROOT)
    #     jsPath = '{0}/js/image-picker.min.js'.format(settings.STATIC_ROOT)
    #     jsPath2 = '{0}/js/image-picker.coffee'.format(settings.STATIC_ROOT)

    #     css = {
    #         'all': (cssPath, cssPath2)
    #     }
    #     js = (jsPath, jsPath2)

    class Media:
        cssPath = '{0}/image-picker/image-picker/image-picker.css'.format(settings.STATIC_ROOT)
        # cssPath2 = '{0}/css/image-picker.scss'.format(settings.STATIC_ROOT)
        jsPath = '{0}/image-picker/image-picker/image-picker.min.js'.format(settings.STATIC_ROOT)
        # jsPath2 = '{0}/js/image-picker.coffee'.format(settings.STATIC_ROOT)

        css = {
            'all': (cssPath,)
        }
        js = (jsPath,)

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
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''

        i = None
        img = None
        if option_value != '':
            i = int(option_value) - 1
            img = self.field_img[i]

        return format_html('<option data-img-src="{}" value="{}"{}>{}</option>',
            img,
            option_value,
            selected_html,
            force_text(option_label)
            )