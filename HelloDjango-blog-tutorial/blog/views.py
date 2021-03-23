import re

from django.shortcuts import render, get_object_or_404
import markdown
# Create your views here.
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.http import HttpResponse
from .models import Post, Category, Tag


def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={
        'post_list': post_list,
    })


def archive(request, year, month):
    print(year, month)
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month,
                                    )
    print(post_list)
    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # post.body = markdown.markdown(Post.body, extensions=[
    #     'markdown.extensions.extra'
    #     'markdown.extensions.codehilite',
    #     'markdown.extensions.toc'
    # ])
    # 阅读量 +1
    post.increase_views()
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 'markdown.extensions.toc',
        # 记得在顶部引入 TocExtension 和 slugify
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'blog/detail.html', context={'post': post})


def category(request, pk):
    # 记得在开始部分导入Category类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})


def tag(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
