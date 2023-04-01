from django.core.paginator import Paginator
from django.db.models import Q, F
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import Category, Post, Tag


def index(request):
    '''# 首页'''
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


@login_required(login_url='/login/')
def home_backend(request):
    '''后台管理首页'''

    # 查询此人的所有文章
    article_list = Post.objects.all()  # 查询到所有的文章,queryset
    '''locals()函数会以字典类型返回当前位置所有的局部变量。'''
    return render(request, 'blog/backend/home.html', locals())


def add_kindeditor(request):
    '''wangeditor 富文本编辑器'''
    if request.method == 'GET':
        article_list = Post.objects.all()
        return render(request, 'blog/backend/add_kindeditor.html', locals())
    else:
        title = request.POST.get('title')
        text_content = request.POST.get('text_content')
        desc = text_content[0:100]
        category_id_list = request.POST.getlist('category_id')
        category_id = category_id_list[0]
        tag_id_list = request.POST.getlist('tag_id')
        '''参数1：要查询的对象， 参数2：查询条件，成功则返回该对象'''
        tag = get_object_or_404(Tag, id=tag_id_list[0])
        print("username, ", request.user.username)
        print("id, ", request.user.id)
        owner_id = request.user.id
        # 数据库， 增加文章数据
        Post.objects.create(title=title,
                            content=text_content,
                            desc=desc,
                            category_id=category_id,
                            owner_id=owner_id,
                            tags=tag)
        # 重定向
        return redirect('/home_backend/')


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


def edit_kindeditor(request, post_id):
    '''
    使用kindeditor，编辑已存在的文章
    ---
    post_id: 文章的id
    '''
    if request.method == 'GET':
        # article_list = Post.objects.all()
        post = get_object_or_404(Post, id=post_id)
        context = {'post':post}
        return render(request, 'blog/backend/edit_kindeditor.html', context)
    else:
        title = request.POST.get('title')
        text_content = request.POST.get('text_content')
        desc = text_content[0:100]
        category_id_list = request.POST.getlist('category_id')
        category_id = category_id_list[0]
        tag_id_list = request.POST.getlist('tag_id')
        '''参数1：要查询的对象， 参数2：查询条件，成功则返回该对象'''
        tag = get_object_or_404(Tag, id=tag_id_list[0])
        print("username, ", request.user.username)
        print("id, ", request.user.id)
        owner_id = request.user.id
        # 数据库， 增加文章数据，不是增加数据，是修改数据，考虑如何修改数据库，数据
        Post.objects.create(title=title,
                            content=text_content,
                            desc=desc,
                            category_id=category_id,
                            owner_id=owner_id,
                            tags=tag)
        # 重定向
        return redirect('/home_backend/')


from django.views.decorators.clickjacking import xframe_options_sameorigin


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

def myadmin(request):
    return render(request, 'admin/index/index.html', locals())

def welcome(request):
    return render(request, 'admin/index/welcome.html', locals())