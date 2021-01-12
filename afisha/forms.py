from django import forms
from mptt.forms import TreeNodeChoiceField
from .models import Category, City

class AdForm(forms.Form):
    stock = forms.BooleanField(label='Aksiýa', widget=forms.CheckboxInput(), required=False)
    category = forms.ModelChoiceField(empty_label='Kategoriýany saýlaň', widget=forms.Select(attrs={"class": "form-control mb-2"}),queryset=Category.objects.all())
    city = TreeNodeChoiceField(empty_label='Şäheri saýlaň', widget=forms.Select(attrs={"class": "form-control mb-3"}),queryset=City.objects.all())

class ContactForm(forms.Form):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"placeholder": "Adyňyz"}))
    email = forms.EmailField(max_length=150, widget=forms.EmailInput(attrs={"placeholder": "Email salgyňyz"}))
    subject = forms.CharField(max_length=250, widget=forms.TextInput(attrs={"placeholder": "Tema"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 6, "placeholder": "Teklibiňiz"}))