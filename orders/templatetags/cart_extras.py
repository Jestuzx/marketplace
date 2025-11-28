from django import template

register = template.Library()

@register.filter
def dict_key(dictionary, key):
    """Возвращает значение по ключу словаря"""
    return dictionary.get(str(key), 0)
