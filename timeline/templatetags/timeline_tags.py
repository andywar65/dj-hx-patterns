from django import template

register = template.Library()


@register.simple_tag
def draw_bar_chart(phase, year, month):
    return phase.draw_bar_chart(year, month)
