from django import template

register = template.Library()

@register.inclusion_tag('users/auth_form.html')
def show_auth(url, form_type, form):
    return {'url': url, 'type': form_type, 'form': form}