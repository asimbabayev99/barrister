from django import template
from dateutil import parser
import datetime
register = template.Library()

weekdays = {1:"Bazar ertəsi",2:"Çərşənbə axşamı",3:"Çərşənbə",4:"Cümə axşamı",5:"Cümə",6:"Şənbə",7:"Bazar"}
months = {1:"Yanvar",2:"Fevral",3:"Mart",4:"Aprel",5:"May",6:"Iyun",7:"Iyul",8:"Avqust",9:"Sentyabr",10:"Oktyabr",11:"Noyabr",12:"Dekabr"}
@register.filter
def date_with_week(value):
    print(value.weekday())
    date_string = "%s %s %s,%s"%(value.day,months[value.month],value.year,weekdays[value.weekday()])
    return date_string