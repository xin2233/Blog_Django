from django.core.paginator import Paginator
from django.db.models import Q, F, Sum
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

# Create your views here.
from .models import Category, Post, Tag


def index(request):
    '''# 首页'''
    post_list = Post.objects.all().order_by('-id')  # 查询到所有的文章,queryset
    # 分页方法
    paginator = Paginator(post_list, 2)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')  # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


def category_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    # 获取当前分类下的所有文章
    posts = category.post_set.all().order_by('-id')
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

    context = {'post': post, 'prev_post': prev_post, 'next_post': next_post}
    return render(request, 'blog/detail.html', context)


def search(request):
    """ 搜索视图 """
    keyword = request.GET.get('keyword')
    # 没有搜索默认显示所有文章
    if not keyword:
        post_list = Post.objects.all().order_by('-id')
    else:
        # 包含查询的方法，用Q对象来组合复杂查询，title__icontains 他两个之间用的是双下划线（__）链接
        post_list = Post.objects.filter(
            Q(title__icontains=keyword) | Q(desc__icontains=keyword) | Q(content__icontains=keyword)).order_by('-id')
    paginator = Paginator(post_list, 2)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')  # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'blog/index.html', context)


def archives(request, year, month):
    # 文章归档列表页
    post_list = Post.objects.filter(add_date__year=year, add_date__month=month).order_by('-id')
    paginator = Paginator(post_list, 2)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')  # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'year': year, 'month': month}
    return render(request, 'blog/archives_list.html', context)


from django.contrib.auth.decorators import login_required


@login_required(login_url='users:login')
def home_backend(request):
    """后台文章列表。"""
    query = request.GET.get('q', '').strip()
    article_list = Post.objects.select_related('category', 'owner', 'tags').order_by('-pub_date')
    if query:
        article_list = article_list.filter(Q(title__icontains=query) | Q(desc__icontains=query))
    paginator = Paginator(article_list, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    stats = Post.objects.aggregate(total_views=Sum('pv'))
    context = {
        'page_obj': page_obj,
        'article_count': article_list.count(),
        'total_views': stats['total_views'] or 0,
        'query': query,
    }
    return render(request, 'blog/backend/home.html', context)


@login_required(login_url='users:login')
def add_kindeditor(request):
    """创建文章。"""
    context = {"categories": Category.objects.all(), "tags": Tag.objects.all()}
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('text_content', '').strip()
        category_id = request.POST.get('category_id')
        tag_id = request.POST.get('tag_id') or None
        if not title or not content or not category_id:
            context["error"] = "请填写标题、正文和分类。"
            return render(request, 'blog/backend/add_kindeditor.html', context)
        Post.objects.create(title=title, content=content, desc=content[:200], category_id=category_id, owner=request.user, tags_id=tag_id)
        return redirect('blog:home_backend')
    return render(request, 'blog/backend/add_kindeditor.html', context)


from django.conf import settings  # 配置文件
from django.views.decorators.csrf import csrf_exempt  # 取消csrftoken
import os


@csrf_exempt
def uploadimg(request):
    '''上传图片在富文本编辑器中, 是ckeditor5的富文本编辑器，用于在admin 的文章管理页面'''
    res = {
        "errno": 0,  # // 注意：值是数字，不能是字符串
        "data": {
            "url": "/media/upload/img/",  # // 图片 src ，必须
            "alt": "yyy",  # // 图片描述文字，非必须
            "href": "zzz"  # // 图片的链接，非必须
        }
    }
    res_err = {
        "errno": 1,  # 只要不等于 0 就行
        "message": "失败信息"
    }
    # print(request.FILES)
    file = request.FILES.get('custom-field-name')
    # print(file.name)
    try:
        new_path = os.path.join(settings.MEDIA_ROOT, 'upload/img/', file.name)
        with open(new_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

            # 成功 settings.MEDIA_URL
            res['data']['url'] = '/media/upload/img/' + file.name

        print('success:', res)
        return JsonResponse(res)
    except IOError:
        res_err['message'] = "图片上传失败！"
        print("error:", res_err)
        return JsonResponse(res_err)


@login_required(login_url='users:login')
def edit_kindeditor(request, post_id):
    """编辑指定文章。"""
    post = get_object_or_404(Post, id=post_id)
    context = {"post": post, "categories": Category.objects.all(), "tags": Tag.objects.all()}
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('text_content', '').strip()
        category_id = request.POST.get('category_id')
        tag_id = request.POST.get('tag_id') or None
        if not title or not content or not category_id:
            context["error"] = "请填写标题、正文和分类。"
            return render(request, 'blog/backend/edit_kindeditor.html', context)
        post.title = title
        post.content = content
        post.desc = content[:200]
        post.category_id = category_id
        post.tags_id = tag_id
        post.save()
        return redirect('blog:home_backend')
    return render(request, 'blog/backend/edit_kindeditor.html', context)


from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.http import require_POST
from django.http import JsonResponse


@login_required(login_url='users:login')
@require_POST
def delete_article(request, post_id):
    """删除文章（仅限自己的文章）。"""
    post = get_object_or_404(Post, id=post_id, owner=request.user)
    post.delete()
    messages.success(request, '文章「{}」已删除。'.format(post.title))
    return redirect('blog:home_backend')


@login_required(login_url='users:login')
@require_POST
def ajax_create_category(request):
    """AJAX 新建分类。"""
    name = request.POST.get('name', '').strip()
    if not name:
        return JsonResponse({'error': '分类名称不能为空'}, status=400)
    if Category.objects.filter(name=name).exists():
        return JsonResponse({'error': '分类「{}」已存在。'.format(name)}, status=400)
    category = Category.objects.create(name=name)
    return JsonResponse({'id': category.id, 'name': category.name})


@login_required(login_url='users:login')
@require_POST
def ajax_create_tag(request):
    """AJAX 新建标签。"""
    name = request.POST.get('name', '').strip()
    if not name:
        return JsonResponse({'error': '标签名称不能为空'}, status=400)
    if Tag.objects.filter(name=name).exists():
        return JsonResponse({'error': '标签「{}」已存在。'.format(name)}, status=400)
    tag = Tag.objects.create(name=name)
    return JsonResponse({'id': tag.id, 'name': tag.name})


@login_required(login_url='users:login')
def category_tag_manager(request):
    """分类/标签管理页面。"""
    categories = Category.objects.all().order_by('id')
    tags = Tag.objects.all().order_by('id')
    return render(request, 'blog/backend/category_tag_manager.html', {
        'categories': categories,
        'tags': tags,
    })


@login_required(login_url='users:login')
@require_POST
def ajax_update_category(request):
    """AJAX 重命名分类。"""
    category_id = request.POST.get('id')
    name = request.POST.get('name', '').strip()
    if not category_id or not name:
        return JsonResponse({'error': '参数不完整'}, status=400)
    if Category.objects.filter(name=name).exclude(id=category_id).exists():
        return JsonResponse({'error': '分类名称「{}」已存在。'.format(name)}, status=400)
    category = get_object_or_404(Category, id=category_id)
    category.name = name
    category.save()
    return JsonResponse({'id': category.id, 'name': category.name})


@login_required(login_url='users:login')
@require_POST
def ajax_delete_category(request):
    """AJAX 删除分类。"""
    category_id = request.POST.get('id')
    category = get_object_or_404(Category, id=category_id)
    if category.post_set.exists():
        return JsonResponse({'error': '分类「{}」下还有文章，无法删除。'.format(category.name)}, status=400)
    category.delete()
    return JsonResponse({'ok': True})


@login_required(login_url='users:login')
@require_POST
def ajax_update_tag(request):
    """AJAX 重命名标签。"""
    tag_id = request.POST.get('id')
    name = request.POST.get('name', '').strip()
    if not tag_id or not name:
        return JsonResponse({'error': '参数不完整'}, status=400)
    if Tag.objects.filter(name=name).exclude(id=tag_id).exists():
        return JsonResponse({'error': '标签名称「{}」已存在。'.format(name)}, status=400)
    tag = get_object_or_404(Tag, id=tag_id)
    tag.name = name
    tag.save()
    return JsonResponse({'id': tag.id, 'name': tag.name})


@login_required(login_url='users:login')
@require_POST
def ajax_delete_tag(request):
    """AJAX 删除标签。"""
    tag_id = request.POST.get('id')
    tag = get_object_or_404(Tag, id=tag_id)
    tag.delete()
    return JsonResponse({'ok': True})


@csrf_exempt
@xframe_options_sameorigin
def kindeditor_upload_img(request):
    '''
    kindeditor 富文本编辑器 图片编辑
    '''

    '''
    有关X-Frame-Options
    2.1 什么是X-Frame-Options
    X-Frame-Options HTTP 响应头是用来给浏览器指示允许一个页面可否在 , 或者
    2.2 X-Frame-Options选项
    X-Frame-Options 有三个值:

    DENY ：表示该页面不允许在 frame 中展示，即便是在相同域名的页面中嵌套也不允许
    SAMEORIGIN ：表示该页面可以在相同域名页面的 frame 中展示
    ALLOW-FROM uri ：表示该页面可以在指定来源的 frame 中展示
    换一句话说，如果设置为 DENY，不光在别人的网站 frame 嵌入时会无法加载，在同域名页面中同样会无法加载。
    另一方面，如果设置为 SAMEORIGIN，那么页面就可以在同域名页面的 frame 中嵌套。
    '''

    # // 成功时
    res = {
        "error": 0,
        "url": "/media/upload/img/"
    }
    # // 失败时
    res_error = {
        "error": 1,
        "message": "错误信息"
    }

    # print(request.FILES)
    file = request.FILES.get('imgFile')
    # print(file.name)

    try:
        new_path = os.path.join(settings.MEDIA_ROOT, 'upload/img/', file.name)
        with open(new_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

            # 成功 settings.MEDIA_URL
            res['url'] = '/media/upload/img/' + file.name

        print('success:', res)
        return JsonResponse(res)
    except IOError:
        res_error['message'] = "图片上传失败！"
        print("error:", res_error)
        return JsonResponse(res_error)
