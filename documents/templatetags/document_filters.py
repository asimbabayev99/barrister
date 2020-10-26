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

    suffix = ""
    date = datetime.strptime(value, '%Y-%m-%d').date()
    mod = date.year % 10
    if mod == 6:
        suffix = "-cı"
    elif mod == 3 or mod == 4:
        suffix = "-cü"
    elif mod == 0:
        suffix = "-ci"
        mod = date.year % 100
        suffix = "-cü" if date.year % 1000 > 0 else suffix
        suffix = "-cı" if mod in [40, 60, 90] else suffix
        suffix = "-ci" if mod in [20, 50, 70, 80] else suffix
        suffix = "-cu" if mod in [10, 30] else suffix
    elif mod == 9:
        suffix = "-cu"
    else: 
        suffix = "-ci"

    return datetime.strftime(date, "%d.%m.%Y") + suffix



@register.filter
def to_list(value, i):
    if not value:
        return "_"*10

    value = value.split()
    if i >= len(value):
        return "_"*10
    else:
        return value[i]


@register.filter
def if_any(value, key):
    if not value:
        return False
    for i in value:
        if i.get(key):
            return True
    return False

    
@register.filter
def subtract_date(value):
    date = datetime.strptime(value, '%Y-%m-%d').date()



@register.filter
def update_variable(value):
    data = value
    return data



class SetVarNode(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value

        return ""


@register.tag(name='set')
def set_var(parser, token):
    """
    {% set some_var = '123' %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form: {% set <var_name> = <var_value> %}")

    return SetVarNode(parts[1], parts[3]) 