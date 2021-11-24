import datetime
from django.core.mail import send_mail
from django.db.models import F
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import ListView, DetailView, FormView, RedirectView
from django.conf import settings
from .models import *
from .forms import *
from django.utils.translation import ugettext as _

adt = Ad.objects.filter(disabled=False)

recent_cat = list()
for category in Category.objects.all():
    ads = adt.filter(category=category).count()
    if ads >0:
        recent_cat.append(adt.filter(category=category)[0])

context_global = dict(category=Category.objects.all(), cities=City.objects.all(), LANGUAGES=settings.LANGUAGES,
                      current_date=datetime.datetime.now(), social=SocialNetworks.objects.all(), description='')

def index(request):
    context = context_global
    context["recent_cat"] = recent_cat
    context["recent_ads"] = adt.all()[:3]
    context["title"] = _('Saýla')
    context['ad_class'] = 'col-lg-12'
    context['description'] = _('Saýla web sahypasy size mahabat hyzmatlaryny hödürleýär. Siz web sahypamyzdan islendik hyzmatlar ugrunda işleýän islendik hususy kärhanalar, dükanlar, kafeler we ş.m. hakynda maglumat tapyp bilersiňiz')
    return render(request, 'afisha/index.html', context=context)

def error_404(request, exception):
    context = context_global
    context["title"] = _('Beýle sahypa ýok!')
    context["content"] = _('Bagyşlaň, siziň gözleýän sahypaňyz ýa-da postlaryňyz saýtymyzda ýok!')
    return render(request, 'error.html', context, status=404)

def error_403(request, exception):
    context = context_global
    context["title"] = _('Bu sahypa girmek gadagan!')
    context["content"] = _('Bagyşlaň, size bu sahypa girmek gadagandyr!')
    return render(request, 'error.html', context)

def error_500(request):
    context = context_global
    context["title"] = _('Serwer ýalňyşlygy')
    context["content"] = _('Bagyşlaň, siz bu sahypa girjek bolan wagtyňyz, serwerde ýalňyşlyk ýüze çykdy! Öý sahypa ýa-da öňki sahypaňyza dolanmagyňyzy haýyyş edýäris!')
    return render(request, 'error.html', context)

class AdView(ListView):
    template_name = 'afisha/ad.html'
    context_object_name = 'ads'
    paginate_by = 4

    def get_queryset(self):
        form = AdForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data
            return get_list_or_404(adt.filter(stock=data['stock'], category=data['category'], city=data['city']))
        return adt.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(context_global)
        context['title'] = _('Postlar')
        context['q'] = ''
        context['form'] = AdForm()
        context['ad_class'] = 'col-lg-6'
        context['description'] = _('Postlaryň, mahabatlaryň toplumy bilen tanyş boluň')
        return context

class AdsByCategory(AdView):
    def get_queryset(self):
        return get_list_or_404(adt.filter(category__slug=self.kwargs['slug']))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug']).name
        context['description'] = Category.objects.get(slug=self.kwargs['slug']).description
        return context

class AdsByCity(AdView):

    def get_queryset(self):
        return get_list_or_404(adt.filter(city__slug=self.kwargs['slug']))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = City.objects.get(slug=self.kwargs['slug']).name
        context['description'] = City.objects.get(slug=self.kwargs['slug']).description
        return context

class StocksView(AdView):

    def get_queryset(self):
        return get_list_or_404(adt.filter(stock=True))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Aksiýalar')
        context['description'] = _('Web sahypamyzdan dürli, hereket edýän aksiýalar bilen tanyş boluň')
        return context

class GetAd(DetailView):
    model = Ad
    template_name = 'afisha/details.html'
    context_object_name = 'ad'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(context_global)
        context['title'] = self.object.title
        self.object.views = F('views')+1
        self.object.save()
        self.object.refresh_from_db()
        return context

class PopularAds(AdView):
    def get_queryset(self):
        return adt.order_by('-ratings__average','-views',)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Meşhur postlar')
        context['description'] = _('Saýtymyzyň iň meşhur postlary, aksiýalary bilen tanyş boluň')
        return context

class Search(AdView):
    def get_queryset(self):
        return get_list_or_404(adt.filter(title__icontains=self.request.GET.get('q')))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Gözleg'),
        context['description'] = _('Gözleg sahypasynda siz gözleýän kafeňyzy, dükanyňyzy tapyp bilersiňiz')
        context['q'] = f"q={self.request.GET.get('q')}&"
        return context

class ContactView(FormView):
    template_name = 'afisha/contact.html'
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        message = name + " şu email-dan: " + email + ", şu haty ugratdy:\n\n" + message;
        send_mail(subject, message, settings.EMAIL_HOST_USER, ['saylapal@gmail.com'], fail_silently=True)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(context_global)
        context['phone'] = '+99361771678, +99362939148'
        context['email'] = 'saylapal@gmail.com'
        context['description'] = _('Biz bilen habarlaşmak arkaly siz bize saýtymyzy kämilleşdirmekde kömek etýäňiz')
        return context

class CounterRedirectView(RedirectView):
    permanent = True
    query_string = False
    pattern_name = 'ad-details'

    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, slug=kwargs['slug'])
        ad.phone_counter = F('phone_counter') + 1
        ad.save()
        ad.refresh_from_db()
        return super().get_redirect_url(*args, **kwargs)