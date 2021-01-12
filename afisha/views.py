from django.core.mail import send_mail
from django.db.models import F
from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from django.conf import settings
from .models import *
from .forms import *

recent_cat = list()
for category in Category.objects.all():
    ads = Ad.objects.filter(category=category).count()
    if ads>0:
        recent_cat.append(Ad.objects.filter(category=category)[0])

context_global = {
    "category": Category.objects.all(),
    "cities": City.objects.all(),
}

def index(request):
    context_global["recent_cat"] = recent_cat
    context_global["recent_ads"] = Ad.objects.all()[:3]
    context_global["title"] = 'Türkmen Afişa'
    context_global['ad_class'] = 'col-lg-12'
    return render(request,'afisha/index.html', context=context_global)

class AdView(ListView):
    template_name = 'afisha/ad.html'
    context_object_name = 'ads'
    paginate_by = 4

    def get_queryset(self):
        form = AdForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data
            return Ad.objects.filter(stock=data['stock'], category=data['category'], city=data['city'])
        return Ad.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(context_global)
        context['title'] = 'Mahabatlar'
        context['q'] = ''
        context['form'] = AdForm()
        context['ad_class'] = 'col-lg-6'
        return context

class AdsByCategory(AdView):
    def get_queryset(self):
        return Ad.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context

class AdsByCity(AdView):

    def get_queryset(self):
        return Ad.objects.filter(city__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = City.objects.get(slug=self.kwargs['slug'])
        return context

class StocksView(AdView):

    def get_queryset(self):
        return Ad.objects.filter(stock=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Aksiýalar'
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
        return Ad.objects.order_by('-views', '-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Meşhur mahabatlar'
        return context

class Search(AdView):
    def get_queryset(self):
        return Ad.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Gözleg'
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
        message = name + " with the email, " + email + ", sent the following message:\n\n" + message;
        send_mail(subject, message, settings.EMAIL_HOST_USER, ['begli.geld.08.12.01@gmail.com'], fail_silently=False)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(context_global)
        return context