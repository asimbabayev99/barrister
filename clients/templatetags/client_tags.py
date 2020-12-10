from django import template
import datetime
register = template.Library()

@register.filter
def date_with_week(value):
    date = datetime.datetime.strptime(value)
    print(date.weekday())
    return value