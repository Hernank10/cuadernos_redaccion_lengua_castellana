from django import template

register = template.Library()

@register.filter
def dict_key(dictionary, key):
    """Retorna el valor de un diccionario usando una clave"""
    try:
        if dictionary and key in dictionary:
            return dictionary[key]
    except:
        pass
    return False

@register.filter
def get_item(dictionary, key):
    """Sinónimo de dict_key"""
    try:
        if dictionary and key in dictionary:
            return dictionary[key]
    except:
        pass
    return False
