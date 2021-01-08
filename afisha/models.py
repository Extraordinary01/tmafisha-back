from django.db import models
from mptt.models import MPTTModel, TreeManyToManyField, TreeForeignKey

class Ad(models.Model):
    title = models.CharField(max_length=200, verbose_name='Mahabatyň ady')
    slug = models.SlugField(max_length=200, verbose_name='URL')
    image = models.ImageField(upload_to="photos/%Y/%m/%d", blank=True, verbose_name='Surat')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Döredilen wagt')
    cities = TreeManyToManyField(City, on_delete=models.CASCADE, null=True, blank=True, related_name='cities', verbose_name='Shaher')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, related_name='category', verbose_name='Kategoriýa')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Mahabat'
        verbose_name_plural = 'Mahabatlar'
        ordering = ['-created_at', 'title']


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Kategoriýanyň ady')
    slug = models.SlugField(max_length=150, verbose_name='URL')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategoriýa'
        verbose_name_plural = 'Kategoriýalar'


class City(MPTTModel):
    name = models.CharField(max_length=100, verbose_name='Shaheriň ady')
    slug = models.SlugField(max_length=100, verbose_name='URL')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, related_name='children')

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Shaher'
        verbose_name_plural = 'Shaherler'

    class MPTTMeta:
        order_insertion_by = ['name']