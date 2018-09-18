from django.contrib.admin import register
from modeltranslation.translator import translator, TranslationOptions
from doctor.models import *
from django.contrib.flatpages.models import FlatPage

class DoctorTranslationOption(TranslationOptions):
    fields = ('pasient_types', 'work_place', 'job_description', 'description', 'education', 'goals')


translator.register(Doctor, DoctorTranslationOption)

# @register(Xestelik)
class XestelikTranslationOption(TranslationOptions):
    fields = ('name',)
    required_languages = ('az', 'ka', 'ru')
translator.register(Xestelik, XestelikTranslationOption)

class StaticPageTranslationOption(TranslationOptions):
    fields = ('title','content',)
    required_languages = ('az', 'ka', 'ru')
translator.register(StaticPage, StaticPageTranslationOption)

class CountryTranslationOption(TranslationOptions):
    fields = ('name',)
    required_languages = ('az', 'ka', 'ru')
translator.register(Country, CountryTranslationOption)

# class StaticPageTranslationOption(TranslationOptions):
#     fields = ('title','content',)
#     required_languages = ('az', 'ka', 'ru')
# translator.register(StaticPage, StaticPageTranslationOption)
