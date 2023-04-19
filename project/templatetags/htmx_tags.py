from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def htmx_url():
    return mark_safe(
        '<script src="https://unpkg.com/htmx.org@1.9.0"\n'
        'integrity="sha384-aOxz9UdWG0yBiyrTwPeMibmaoq07/d3a96GCbb9x60f3mOt5zwkjdbcHFnKH8qls"\n'  # noqa
        'crossorigin="anonymous"></script>'
    )
