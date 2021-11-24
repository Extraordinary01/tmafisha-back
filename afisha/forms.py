from django import forms
from mptt.forms import TreeNodeChoiceField
from .models import Category, City
from django.utils.translation import ugettext_lazy as _

class AdForm(forms.Form):
    stock = forms.BooleanField(label=_('Aksiýa'), widget=forms.CheckboxInput(), required=False)
    category = forms.ModelChoiceField(label=_('Kategoriýa'),empty_label=_('Kategoriýany saýlaň'), widget=forms.Select(attrs={"class": "form-control mb-2"}),queryset=Category.objects.all())
    city = TreeNodeChoiceField(label=_('Şäher'),empty_label=_('Şäheri saýlaň'), widget=forms.Select(attrs={"class": "form-control mb-3"}),queryset=City.objects.all())

class ContactForm(forms.Form):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"placeholder": _("Adyňyz"), "class": "form-control"}))
    email = forms.EmailField(max_length=150, widget=forms.EmailInput(attrs={"placeholder": _("Email salgyňyz"), "class": "form-control"}))
    subject = forms.CharField(max_length=250, widget=forms.TextInput(attrs={"placeholder": _("Tema"), "class": "form-control"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 6, "placeholder": _("Teklibiňiz"), "class": "form-control"}))