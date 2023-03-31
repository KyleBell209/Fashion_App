from django import template

register = template.Library()

@register.filter
def filter(qs, **kwargs):
    return qs.filter(**kwargs)