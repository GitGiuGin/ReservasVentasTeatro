from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Retorna el valor de un diccionario dado su key"""
    return dictionary.get(key)