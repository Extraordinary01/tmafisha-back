from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter
from modeltranslation.admin import TranslationAdmin
from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.translation import ugettext as _
from orderable.admin import OrderableAdmin

class CategoryAdmin(TranslationAdmin):
    prepopulated_fields = {"slug": ("name",)}
    save_on_top = True
    list_display = ('id', 'name', 'description', 'slug')
    list_display_links = ('id', 'name')

class CityAdmin(DraggableMPTTAdmin, TranslationAdmin):
    prepopulated_fields = {"slug": ("name",)}
    save_on_top = True
    list_display = ('tree_actions','indented_title',)
    list_display_links = ('indented_title',)

class AdAdminForm(forms.ModelForm):
    content_tk = forms.CharField(widget=CKEditorUploadingWidget())
    content_ru = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Ad
        fields = '__all__'

class AdAdmin(OrderableAdmin, TranslationAdmin):
    form = AdAdminForm
    prepopulated_fields = {"slug": ("title",)}
    save_on_top = True
    list_display = ('id', 'title', 'description', 'slug', 'stock', 'city', 'category', 'created_at', 'get_image', 'sort_order_display')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('category', ('city', TreeRelatedFieldListFilter), 'stock')
    readonly_fields = ('created_at', 'views', 'get_image', 'phone_counter')
    fields = ('title', 'description', 'slug', 'city', 'category', 'content', 'image', 'get_image', 'stock', 'views', 'created_at', 'phone', 'phone_counter')


    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50px" ></img>')
        return '-'
    get_image.short_description = _('Surat')

class SocialNetworksAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name')

admin.site.register(Category, CategoryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(SocialNetworks, SocialNetworksAdmin)