from modeltranslation.translator import register, TranslationOptions
from .models import *

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

@register(Ad)
class AdTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'content',)