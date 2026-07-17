"""后台管理视图 — 从 views.py 拆分出来"""
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.http import require_POST
import os

from .models import Category, Post, Tag


@login_required(login_url='users:login')
def home_backend(request):
    """后台文章列表。"""
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '')
    article_list = Post.objects.select_related('category', 'owner', 'tags').order_by('-pub_date')
    if status_filter in ('draft', 'published'):
        article_list = article_list.filter(status=status_filter)
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
        'status_filter': status_filter,
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
        status = request.POST.get('status', 'draft')
        if not title or not content or not category_id:
            context["error"] = "请填写标题、正文和分类。"
            return render(request, 'blog/backend/add_kindeditor.html', context)
        Post.objects.create(
            title=title, content=content, desc=content[:200],
            category_id=category_id, owner=request.user, tags_id=tag_id,
            status=status,
        )
        msg = '文章已发布。' if status == 'published' else '文章已保存为草稿。'
        messages.success(request, msg)
        return redirect('blog:home_backend')
    return render(request, 'blog/backend/add_kindeditor.html', context)


@csrf_exempt
def uploadimg(request):
    """上传图片在富文本编辑器中, 是ckeditor5的富文本编辑器，用于在admin 的文章管理页面"""
    res = {
        "errno": 0,
        "data": {
            "url": "/media/upload/img/",
            "alt": "yyy",
            "href": "zzz"
        }
    }
    res_err = {
        "errno": 1,
        "message": "失败信息"
    }
    file = request.FILES.get('custom-field-name')
    try:
        new_path = os.path.join(settings.MEDIA_ROOT, 'upload/img/', file.name)
        with open(new_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
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
        status = request.POST.get('status', post.status)
        if not title or not content or not category_id:
            context["error"] = "请填写标题、正文和分类。"
            return render(request, 'blog/backend/edit_kindeditor.html', context)
        post.title = title
        post.content = content
        post.desc = content[:200]
        post.category_id = category_id
        post.tags_id = tag_id
        post.status = status
        post.save()
        msg = '文章已更新并发布。' if status == 'published' else '文章已保存为草稿。'
        messages.success(request, msg)
        return redirect('blog:home_backend')
    return render(request, 'blog/backend/edit_kindeditor.html', context)


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
def toggle_article_status(request, post_id):
    """一键切换文章状态 draft ↔ published。"""
    post = get_object_or_404(Post, id=post_id, owner=request.user)
    post.status = 'published' if post.status == 'draft' else 'draft'
    post.save()
    status_name = '已发布' if post.status == 'published' else '草稿'
    messages.success(request, '文章「{}」已切换为{}。'.format(post.title, status_name))
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
    """
    kindeditor 富文本编辑器 图片上传
    """
    res = {
        "error": 0,
        "url": "/media/upload/img/"
    }
    res_error = {
        "error": 1,
        "message": "错误信息"
    }
    file = request.FILES.get('imgFile')
    try:
        new_path = os.path.join(settings.MEDIA_ROOT, 'upload/img/', file.name)
        with open(new_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
            res['url'] = '/media/upload/img/' + file.name
        print('success:', res)
        return JsonResponse(res)
    except IOError:
        res_error['message'] = "图片上传失败！"
        print("error:", res_error)
        return JsonResponse(res_error)