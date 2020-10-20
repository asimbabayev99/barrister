from django import template

register = template.Library()

@register.filter
def is_null(value, n):
    if value:
        return value
    else:
        return "_"*n
