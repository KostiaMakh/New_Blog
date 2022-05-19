from django import template

register = template.Library()


@register.inclusion_tag('blog/pagination_tpl.html')
def show_pagination(page_obj):
    return {'page_obj': page_obj}
