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

    def __init__(self, attrs=None, choices=(), form_instance=None):
        super(ImageSelect, self).__init__(attrs)
        self.choices = list(choices)
        self.form_instance = form_instance
        print self.form_instance

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
        return format_html('<option data-img-src="" value="{}"{}>{}</option>',
            option_value,
            selected_html,
            force_text(option_label)
            )