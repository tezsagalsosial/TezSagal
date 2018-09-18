from django import template
from doctor.models import Country, Xestelik
register = template.Library()

@register.filter
def dec_round(value):
    return round(value,0)
@register.filter
def split7(value):
    text = value.split()
    n = 7
    text_s = ''
    list = [' '.join(text[i:i + n]) for i in range(0, len(text), n)]
    i = 1
    for item in list:
        if i==1:
            text_s += item
        else:
            text_s += '<br>'+item
        i+=1
    return text_s