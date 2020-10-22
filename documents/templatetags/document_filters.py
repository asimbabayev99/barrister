from django import template
from datetime import datetime, date
from dateutil import parser

register = template.Library()

@register.filter
def is_null(value, n):
    if value:
        return value
    else:
        return "_"*n


@register.filter
def year_suffix(value):
    if not value:
        return "X.X.X-ci"

    date = datetime.strptime(value, '%Y-%m-%d').date()
    mod = date.year % 10
    if mod == 1 or mod == 2 or mod == 5 or mod == 7 or mod == 8:
        suffix = "-ci"
    elif mod == 0 or mod == 6:
        suffix = "-cı"
    elif mod == 3 or mod == 4:
        suffix = "-cü"
    else:
        suffix = "-cu"

    return datetime.strftime(date, "%d.%m.%Y") + suffix



@register.filter
def to_list(value, i):
    if not value:
        return "-"*10

    value = value.split()
    if i >= len(value):
        return "-"*10
    else:
        return value[i]