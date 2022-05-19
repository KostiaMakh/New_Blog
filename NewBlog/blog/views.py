from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *
from django.db.models import F, Count


class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Classic blog Design'
        return context


class Single_post(DetailView):
    model = Post
    template_name = 'blog/single.html'
    context_object_name = 'post'
    extra_context = {
        'get_all_tags': Tag.objects.annotate(cat=Count('posts', filter=F('posts__tags'))).filter(cat__gt=0)}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


def index(request):
    return render(request, 'blog/index.html')


class Posts_by_category(ListView):
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    paginate_by = 16
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])


class Posts_by_tag(ListView):
    template_name = 'blog/tag_page.html'
    context_object_name = 'posts'
    paginate_by = 16
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])


def get_category(request, slug):
    return render(request, 'blog/category.html')


def get_post(request, slug):
    return render(request, 'blog/post.html')


# Форма поимка статей по названию
class Search_post(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('search_field'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_field'] = f"s={self.request.GET.get('search_field')}&"
        return context
