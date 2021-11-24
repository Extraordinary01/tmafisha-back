from PIL import Image
from django.db import models
from django.urls import reverse_lazy
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext as _
from orderable.models import Orderable
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('Kategoriýanyň ady'))
    description = models.CharField(max_length=150, verbose_name=_('Düşündiriş'), default='')
    slug = models.SlugField(max_length=200, verbose_name='URL', unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('category', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = _('Kategoriýa')
        verbose_name_plural = _('Kategoriýalar')


class City(MPTTModel):
    name = models.CharField(max_length=100, verbose_name=_('Şäheriň ady'))
    description = models.CharField(max_length=150, verbose_name=_('Düşündiriş'), default='')
    slug = models.SlugField(max_length=100, verbose_name='URL', unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('city', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = _('Şäher')
        verbose_name_plural = _('Şäherler')

    class MPTTMeta:
        order_insertion_by = ['name']

class Ad(Orderable):
    title = models.CharField(max_length=200, verbose_name=_('Postyň ady'))
    description = models.CharField(max_length=150, verbose_name=_('Düşündiriş'), default='')
    slug = models.SlugField(max_length=200, verbose_name='URL', unique=True)
    image = models.ImageField(upload_to="photos/%Y/%m/%d", default='default.jpg', verbose_name='Surat')
    content = RichTextField(verbose_name=_('Kontent'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Döredilen wagt'))
    stock = models.BooleanField(default=False, verbose_name=_('Aksiýa'), blank=True)
    disabled = models.BooleanField(default=False, verbose_name=_('Blokdamy'), blank=True)
    views = models.PositiveIntegerField(default=0, verbose_name=_('Görlenleriň sany'))
    phone = models.CharField(max_length=30, verbose_name=_('Telefon belgi'), blank=True)
    phone_counter = models.PositiveIntegerField(default=0, verbose_name=_('Jaň düwmesine basylanlaryň samy'))
    ratings = GenericRelation(Rating, related_query_name='ads')
    city = TreeForeignKey(City, on_delete=models.CASCADE, blank=True, related_name='cities', related_query_name='city', verbose_name=_('Şäher'))
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, related_name='categories', related_query_name='category', verbose_name=_('Kategoriýa'))

    def save(self):
        try:
            this = Ad.objects.get(slug=self.slug)
            if this.image != self.image:
                this.image.delete()
        except: pass
        super().save()
        img = Image.open(self.image.path)
        output_size = (640, 426)
        img = img.resize(output_size)
        img.save(self.image.path)

    def get_absolute_url(self):
        return reverse_lazy('ad-details', kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    class Meta(Orderable.Meta):
        verbose_name = _('Post')
        verbose_name_plural = _('Postlar')
        ordering = ['-sort_order']

class SocialNetworks(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Sosial tordaky akkaundyň ady'))
    link = models.URLField(verbose_name=_('URL-y'))

    class Meta:
        verbose_name = _('Sosial tor')
        verbose_name_plural = _('Sosial torlar')