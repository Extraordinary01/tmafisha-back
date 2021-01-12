from PIL import Image
from django.db import models
from django.urls import reverse_lazy
from mptt.models import MPTTModel, TreeForeignKey

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Kategoriýanyň ady')
    slug = models.SlugField(max_length=200, verbose_name='URL', unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('category', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Kategoriýa'
        verbose_name_plural = 'Kategoriýalar'


class City(MPTTModel):
    name = models.CharField(max_length=100, verbose_name='Şäheriň ady')
    slug = models.SlugField(max_length=100, verbose_name='URL', unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('city', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Şäher'
        verbose_name_plural = 'Şäherler'

    class MPTTMeta:
        order_insertion_by = ['name']

class Ad(models.Model):
    title = models.CharField(max_length=200, verbose_name='Mahabatyň ady')
    slug = models.SlugField(max_length=200, verbose_name='URL', unique=True)
    image = models.ImageField(upload_to="photos/%Y/%m/%d", default='default.jpg', verbose_name='Surat')
    content = models.TextField(verbose_name='Kontent')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Döredilen wagt')
    stock = models.BooleanField(default=False, verbose_name='Aksiýa')
    views = models.IntegerField(default=0, verbose_name='Görlenleriň sany')
    city = TreeForeignKey(City, on_delete=models.CASCADE, blank=True, related_name='cities', related_query_name='city', verbose_name='Şäher')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, related_name='categories', related_query_name='category', verbose_name='Kategoriýa')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        img = Image.open(self.image.path)
        output_size = (426,640)
        img.thumbnail(output_size)
        img.save(self.image.path)

    def get_absolute_url(self):
        return reverse_lazy('ad-details', kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Mahabat'
        verbose_name_plural = 'Mahabatlar'
        ordering = ['-created_at', 'title']