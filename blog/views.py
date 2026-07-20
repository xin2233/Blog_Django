from django.core.paginator import Paginator
from django.db.models import Q, F, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST

# Create your views here.
from .models import Category, Post, Comment


def index(request):
    '''# 首页'''
    post_list = Post.objects.filter(status='published').order_by('-id')  # 查询到所有的文章,queryset
    # 分页方法
    paginator = Paginator(post_list, 2)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')  # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


def category_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    # 获取当前分类下的所有文章
    posts = category.post_set.filter(status='published').order_by('-id')
    paginator = Paginator(posts, 2)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')  # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'page_obj': page_obj}
    return render(request, 'blog/list.html', context)


def post_detail(request, post_id):
    '''文章详情页'''
    post = get_object_or_404(Post, id=post_id)

    # 用文章id来实现的上下篇
    prev_post = Post.objects.filter(id__lt=post_id).last()  # 上一篇
    next_post = Post.objects.filter(id__gt=post_id).first()  # 下一篇
    Post.objects.filter(id=post_id).update(pv=F('pv') + 1)  # 这个功能有漏洞，仅做思路讲解

    # 用发布日期来实现上下篇
    # date_prev_post = Post.objects.filter(add_date__lt=post.add_date).last()
    # date_next_post = Post.objects.filter(add_date__gt=post.add_date).first()

    comments = post.comments.filter(is_approved=True, parent__isnull=True).select_related('author').prefetch_related('comment_set')
    comment_count = post.comments.filter(is_approved=True).count()

    context = {
        'post': post,
        'prev_post': prev_post,
        'next_post': next_post,
        'comments': comments,
        'comment_count': comment_count,
    }
    return render(request, 'blog/detail.html', context)


def search(request):
    """ 搜索视图 """
    keyword = request.GET.get('keyword')
    # 没有搜索默认显示所有文章
    if not keyword:
        post_list = Post.objects.filter(status='published').order_by('-id')
    else:
        # 包含查询的方法，用Q对象来组合复杂查询，title__icontains 他两个之间用的是双下划线（__）链接
        post_list = Post.objects.filter(
            Q(title__icontains=keyword) | Q(desc__icontains=keyword) | Q(content__icontains=keyword),
            status='published').order_by('-id')
    paginator = Paginator(post_list, 2)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')  # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'blog/index.html', context)


def archives(request, year, month):
    # 文章归档列表页
    post_list = Post.objects.filter(status='published', add_date__year=year, add_date__month=month).order_by('-id')
    paginator = Paginator(post_list, 2)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')  # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'year': year, 'month': month}
    return render(request, 'blog/archives_list.html', context)


@require_POST
def submit_comment(request, post_id):
    """提交评论"""
    post = get_object_or_404(Post, id=post_id, status='published')
    content = request.POST.get('content', '').strip()
    parent_id = request.POST.get('parent_id')
    if not content:
        messages.error(request, '评论内容不能为空。')
        return redirect('blog:post_detail', post_id=post_id)

    if len(content) > 1000:
        messages.error(request, '评论内容不能超过1000字。')
        return redirect('blog:post_detail', post_id=post_id)

    if request.user.is_authenticated:
        comment = Comment(post=post, author=request.user, content=content)
    else:
        nickname = request.POST.get('nickname', '').strip() or '匿名'
        comment = Comment(post=post, nickname=nickname, content=content)

    if parent_id:
        parent = get_object_or_404(Comment, id=parent_id, post=post)
        comment.parent = parent

    comment.save()
    messages.success(request, '评论已提交，等待审核后显示。')
    return redirect('blog:post_detail', post_id=post_id)