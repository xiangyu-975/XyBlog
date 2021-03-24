import re

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
import markdown
# Create your views here.
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.http import HttpResponse
from pure_pagination import PaginationMixin

from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView
from django.contrib import messages


class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # 指定paginate_by 属性后开启分页功能，其值代表每一页包含了多少篇文章
    paginate_by = 10


# def index(request):
#     post_list = Post.objects.all()
#     return render(request, 'blog/index.html', context={
#         'post_list': post_list,
#     })

class ArchiveView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'


# def archive(request, year, month):
#     print(year, month)
#     post_list = Post.objects.filter(create_time__year=year,
#                                     create_time__month=month,
#                                     )
#     print(post_list)
#     return render(request, 'blog/index.html', context={'post_list': post_list})

class PostDetailView(DetailView):
    # 这些属性的含义和ListView是一样的
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写get方法的目的是因为每当文章被访问一次，就将文章的阅读量+1
        # get方法返回的是一个HttpResponse实例
        # 之所以需要先调用父类的get方法，是因为只有当get方法被调用后，
        # 才有 self.object属性，其值为 Post 模型实例，即被访问文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        # 将文章阅读量+1
        # 注意self.object的值就是被访问的文章post
        self.object.increase_views()
        # 视图必须返回一个HttpResponse对象
        return response

    def get_object(self, queryset=None):
        # 覆写get_object 方法的目的是因为需要对 post 的body值进行渲染
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)

        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        return post


# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     # post.body = markdown.markdown(Post.body, extensions=[
#     #     'markdown.extensions.extra'
#     #     'markdown.extensions.codehilite',
#     #     'markdown.extensions.toc'
#     # ])
#     # 阅读量 +1
#     post.increase_views()
#     md = markdown.Markdown(extensions=[
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         # 'markdown.extensions.toc',
#         # 记得在顶部引入 TocExtension 和 slugify
#         TocExtension(slugify=slugify),
#     ])
#     post.body = md.convert(post.body)
#     m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
#     post.toc = m.group(1) if m is not None else ''
#     return render(request, 'blog/detail.html', context={'post': post})


class CategoryView(ListView):
    model = Category
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


# def category(request, pk):
#     # 记得在开始部分导入Category类
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate)
#     return render(request, 'blog/index.html', context={'post_list': post_list})

class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tag=tag)


# def tag(request, pk):
#     t = get_object_or_404(Tag, pk=pk)
#     post_list = Post.objects.filter(tags=t).order_by('-create_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})

def search(request):
    q = request.GET.get('q')
    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'post_list': post_list})
