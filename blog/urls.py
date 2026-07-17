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
    path('delete_article/<int:post_id>/', views.delete_article, name='delete_article'),  # 删除文章
    path('kindeditor_upload_img/', views.kindeditor_upload_img, name='kindeditor_upload_img'),  # kindeditor 富文本编辑器 上传图片
    path('ajax_create_category/', views.ajax_create_category, name='ajax_create_category'),  # AJAX 新建分类
    path('ajax_create_tag/', views.ajax_create_tag, name='ajax_create_tag'),  # AJAX 新建标签
    path('category_tag_manager/', views.category_tag_manager, name='category_tag_manager'),  # 分类/标签管理
    path('ajax_update_category/', views.ajax_update_category, name='ajax_update_category'),  # AJAX 重命名分类
    path('ajax_delete_category/', views.ajax_delete_category, name='ajax_delete_category'),  # AJAX 删除分类
    path('ajax_update_tag/', views.ajax_update_tag, name='ajax_update_tag'),  # AJAX 重命名标签
    path('ajax_delete_tag/', views.ajax_delete_tag, name='ajax_delete_tag'),  # AJAX 删除标签

]
