from django import template
from blog.models import Category
from django.db.models import F, Count

register = template.Library()


@register.inclusion_tag('blog/menu_tpl.html')
def show_menu(menu_class='menu'):
    categories = Category.objects.annotate(cat=Count('posts', filter=F('posts__id'))).filter(cat__gt=0)
    # categories = Category.objects.annotate(cat=Count('news', filter=F('news__is_published'))).filter(cat__gt=0)
    return {'categories': categories, 'menu_class': menu_class}
