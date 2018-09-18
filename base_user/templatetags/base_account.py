from django import template
from doctor.models import Country, Xestelik
register = template.Library()


@register.filter
def not_null(arg):
    if arg:
        return arg
    else:
        return ""

@register.filter
def get_country_name(arg):
    try:
        a = Country.objects.get(id=arg)
        return a.name
    except:
        return ""

@register.filter
def get_xestelik_name(arg):
    try:
        a = Xestelik.objects.get(id=arg)
        return a.name
    except:
        return ""

@register.filter
def get_youtube_embed_url(url):
    if url:
        result = 'https://www.youtube.com/embed/' + url[-11:]
        return result
    else:
        return 'https://www.youtube.com/embed/hb04Nh7GxmE'