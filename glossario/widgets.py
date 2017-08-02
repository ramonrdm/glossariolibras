from django.utils.safestring import mark_safe
from django import forms

class ImageSelect(forms.Select):
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
        return format_html('<option data-img-src="/static/img/cinema.jpg" value="{}"{}>{}</option>', option_value, selected_html, force_text(option_label))
