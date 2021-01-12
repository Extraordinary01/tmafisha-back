from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter
from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    save_on_top = True
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')

class CityAdmin(DraggableMPTTAdmin):
    prepopulated_fields = {"slug": ("name",)}
    save_on_top = True
    list_display = ('tree_actions','indented_title',)
    list_display_links = ('indented_title',)

class AdAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Ad
        fields = '__all__'

class AdAdmin(admin.ModelAdmin):
    form = AdAdminForm
    prepopulated_fields = {"slug": ("title",)}
    save_on_top = True
    list_display = ('id', 'title', 'slug', 'stock', 'city', 'category', 'created_at', 'get_image')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('category', ('city', TreeRelatedFieldListFilter), 'stock')
    readonly_fields = ('created_at', 'views', 'get_image')
    fields = ('title', 'slug', 'city', 'category', 'content', 'image', 'get_image', 'stock', 'views', 'created_at')


    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50px" ></img>')
        return '-'
    get_image.short_description = 'Surat'

admin.site.register(Category, CategoryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Ad, AdAdmin)