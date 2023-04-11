from django.urls import path, include

from . import views

app_name = "blog"

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>/', views.category_list, name='category_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('search/', views.search, name='search'),
    path('archives/<int:year>/<int:month>/', views.archives, name='archives'),

    # 后台
    path('home_backend/', views.home_backend, name='home_backend'),  # 后台管理首页
    path('upload_img/', views.uploadimg, name='upload_img'),  # 上穿图片
    path('ckeditor/', include('ckeditor_uploader.urls')),  # 富文本编辑器中的图片上传和存储
    path('add_article/', views.add_kindeditor, name='add_article'),  # 后台新增文章
    path('edit_article/<int:post_id>/', views.edit_kindeditor, name='edit_article'),  # 增加富文本编辑器，编辑已存在文章
    path('kindeditor_upload_img/', views.kindeditor_upload_img, name='kindeditor_upload_img'),  # kindeditor 富文本编辑器 上传图片

    # 新后台
    # ver1
    path('myadmin/', views.myadmin),
    path('welcome/', views.welcome),
    path('menu1/', views.menu1),
    path('menu2/', views.menu2),
    path('article-info/', views.article_info),
    path('article-add/', views.article_add),
    path('article-list/', views.article_list),
    path('article-detail/', views.article_detail),
    path('danye-list/', views.danye_list),

    # ver2
    path('welcome1/', views.welcome1),
    path('base', views.basetest)

]
