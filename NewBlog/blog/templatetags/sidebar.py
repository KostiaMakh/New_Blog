from django import template
from blog.models import Post, Tag
from django.db.models import F, Count

register = template.Library()


@register.inclusion_tag('blog/popular_posts_tpl.html')
def get_popular_posts(cnt=3):
    posts = Post.objects.order_by('-views')[:cnt]
    return {'posts': posts, }


@register.inclusion_tag('blog/tags_cloud_tpl.html')
def get_tags_cloud():
    tags = Tag.objects.annotate(cat=Count('posts', filter=F('posts__tags'))).filter(cat__gt=0)
    return {'tags': tags, }


@register.inclusion_tag('blog/search_tpl.html')
def get_search_block():
    return {}