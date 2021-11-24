from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext as _
from afisha.views import context_global
from django.conf import settings
UserModel = get_user_model()
from .forms import SignUpForm, LoginForm, UserPasswordResetForm, UserPasswordSetForm

def signup(request):
    context = context_global
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # print(form.cleaned_data.keys())
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = _('Email salgyňyzy tassyklaň.')
            message = render_to_string('users/activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
            return render(request, 'users/confirm_email.html', context)
        else:
            context['forms'] = form
            context['type'] = _('Registrasiýa')
    else:
        form = SignUpForm()
        context['forms'] = form
        context['type'] = _('Registrasiýa')
    return render(request, 'users/signup.html', context)


def activate(request, uidb64, token):
    context = context_global
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'users/activation_success.html', context)
    else:
        return render(request, 'users/activation_error.html', context)

class UserLogin(LoginView):
    template_name = 'users/login.html'
    # authentication_form = LoginForm
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(context_global)
        context['type'] = _('Ulgama girmek')
        return context

    def get_success_url(self):
        return reverse('home')

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

class UserLogout(LogoutView):
    template_name = 'users/logout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(context_global)
        return context

    def get_next_page(self):
        return reverse('home')

class UserPasswordReset(PasswordResetView):
    template_name = 'users/reset_password.html'
    form_class = UserPasswordResetForm
    email_template_name = 'users/reset_password_email.html'
    from_email = settings.EMAIL_HOST_USER
    success_url = 'password-reset-done'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(context_global)
        return context

class UserPasswordResetDone(PasswordResetDoneView):
    template_name = 'users/reset_password_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(context_global)
        return context

class UserPasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'users/reset_password_form.html'
    form_class = UserPasswordSetForm
    success_url = 'password-reset-complete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(context_global)
        return context

class UserPasswordResetComplete(PasswordResetCompleteView):
    template_name = 'users/reset_password_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(context_global)
        return context
