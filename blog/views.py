from http.client import HTTPResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, F
from django.core.paginator import Paginator
# Create your views here.
from .models import Category, Post


def index(request):
    # 首页
    post_list = Post.objects.all()  # 查询到所有的文章,queryset
    # 分页方法
    paginator = Paginator(post_list, 2)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')  # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


def category_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    # 获取当前分类下的所有文章
    posts = category.post_set.all()
    paginator = Paginator(posts, 2)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')  # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'page_obj': page_obj}
    return render(request, 'blog/list.html', context)


def post_detail(request, post_id):
    # 文章详情页
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
        post_list = Post.objects.all()
    else:
        # 包含查询的方法，用Q对象来组合复杂查询，title__icontains 他两个之间用的是双下划线（__）链接
        post_list = Post.objects.filter(
            Q(title__icontains=keyword) | Q(desc__icontains=keyword) | Q(content__icontains=keyword))
    paginator = Paginator(post_list, 2)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')  # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'blog/index.html', context)


def archives(request, year, month):
    # 文章归档列表页
    post_list = Post.objects.filter(add_date__year=year, add_date__month=month)
    paginator = Paginator(post_list, 2)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')  # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'year': year, 'month': month}
    return render(request, 'blog/archives_list.html', context)


from django.contrib.auth.decorators import login_required

# 后台管理首页
# @login_required(login_url='/login/')
def home_backend(request):
    # 查询此人的所有文章
    # article_list = Post.objects.filter(owner = request.user.owner)
    article_list = Post.objects.all()  # 查询到所有的文章,queryset
    return render(request, 'blog/backend/home.html', locals())

# 后台文章编辑页面
def backend_add_article(request):
    return render(request, 'blog/backend/add_wangeditor.html', locals())


from django.conf import settings  # 配置文件
from django.views.decorators.csrf import csrf_exempt  # 取消csrftoken
import os


# 上传图片在富文本编辑器中
@csrf_exempt
def uploadimg(request):
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

# 保存富文本编辑器中的文章
def article_save(request):
    pass


# 增加kindeditor 富文本编辑器
@csrf_exempt
def kindeditor(request):
    return render(request, 'blog/backend/add_kindeditor.html', locals())

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

from django.views.decorators.clickjacking import xframe_options_sameorigin
# kindeditor 富文本编辑器 图片编辑
@csrf_exempt
@xframe_options_sameorigin
def kindeditor_upload_img(request):
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
    print(file.name)

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