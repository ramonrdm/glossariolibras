from django import template
from django.template.defaulttags import register

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# @register.filter() 
# def has_group(user, glossario):
#     return user.groups.filter(name=glossario.membros).exists() 