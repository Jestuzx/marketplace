from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))

@register.filter
def calc_total(products, cart):
    total = 0
    for p in products:
        total += p.price * cart.get(str(p.id), 0)
    return total
