from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=50, label=_('Ulanyjy at'), widget=forms.TextInput(attrs={"class": "form-control", "placeholder": _("Ulanyjy adyňyzy giriziň")}))
    email = forms.EmailField(max_length=150, label=_('Email salgy'),widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": _("Email salgyňyzy giriziň")}))
    password1 = forms.CharField(max_length=50, label=_('Parol'),widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": _("Parolyňyzy giriziň")}))
    password2 = forms.CharField(max_length=50, label=_('Parolyňyzy tassyklaň'),widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": _("Parolyňyzyň tassyklamasyny giriziň")}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=50, label=_('Ulanyjy at'), widget=forms.TextInput(attrs={"class": "form-control", "placeholder": _("Ulanyjy adyňyzy giriziň")}))
    password = forms.CharField(max_length=50, label=_('Parolyňyz'),widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": _("Parolyňyzy giriziň")}))

    class Meta:
        model = User
        fields = ('username', 'password')

class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=150, label=_('Email salgy'),widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": _("Email salgyňyzy giriziň")}))

class UserPasswordSetForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, label=_('Täze parolyňyz'), widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": _("Täze parolyňyzy giriziň")}))
    new_password2 = forms.CharField(max_length=50, label=_('Täze parolyňyzyň tassyklamasy'), widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": _("Täze parolyňyziň tassyklamasyny giriziň")}))