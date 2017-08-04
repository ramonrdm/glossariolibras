from __future__ import unicode_literals
from django.forms.widgets import Select 
import copy
import datetime
import re
from itertools import chain
from django.conf import settings
from django.forms.utils import flatatt, to_current_timezone
from django.templatetags.static import static
from django.utils import datetime_safe, formats, six
from django.utils.datastructures import MultiValueDict
from django.utils.dates import MONTHS
from django.utils.deprecation import (
    RemovedInDjango20Warning, RenameMethodsBase,
)
from django.utils.encoding import (
    force_str, force_text, python_2_unicode_compatible,
)
from django.utils.formats import get_format
from django.utils.html import conditional_escape, format_html, html_safe
from django.utils.safestring import mark_safe
from django.utils.six.moves import range
from django.utils.translation import ugettext_lazy

class ImageSelect(Select):

    class Media:
        css = {
            'all': ('css/image-picker.css')
        }
        js = ('js/image-picker.js',)

    # allow_multiple_selected = False

    def __init__(self, attrs=None, choices=()):
        super(ImageSelect, self).__init__(attrs)
        # choices can be any iterable, but we may need to render this widget
        # multiple times. Thus, collapse it into a list so it can be consumed
        # more than once.
        self.choices = list(choices)

    # def __deepcopy__(self, memo):
    #     obj = copy.copy(self)
    #     obj.attrs = self.attrs.copy()
    #     obj.choices = copy.copy(self.choices)
    #     memo[id(self)] = obj
    #     return obj

    # def render(self, name, value, attrs=None):
    #     if value is None:
    #         value = ''
    #     final_attrs = self.build_attrs(attrs, name=name)
    #     output = [format_html('<select{} class="image-picker">', flatatt(final_attrs))]
    #     options = self.render_options([value])
    #     if options:
    #         output.append(options)
    #     output.append('</select>')
    #     return mark_safe('\n'.join(output))

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
        return format_html('<option data-img-src="" value="{}"{}>{}</option>', option_value, selected_html, force_text(option_label))

    # def render_options(self, selected_choices):
    #     # Normalize to strings.
    #     selected_choices = set(force_text(v) for v in selected_choices)
    #     output = []
    #     for option_value, option_label in self.choices:
    #         if isinstance(option_label, (list, tuple)):
    #             output.append(format_html('<optgroup label="{}">', force_text(option_value)))
    #             for option in option_label:
    #                 output.append(self.render_option(selected_choices, *option))
    #             output.append('</optgroup>')
    #         else:
    #             output.append(self.render_option(selected_choices, option_value, option_label))
    #     return '\n'.join(output)
