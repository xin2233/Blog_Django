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
    path('add_article/', views.backend_add_article, name='add_article'),  # 后台新增文章
    path('upload_img/', views.uploadimg, name='upload_img'),  # 上穿图片
    path('ckeditor/', include('ckeditor_uploader.urls')),   # 富文本编辑器中的图片上传和存储

    path('kindeditor/', views.kindeditor, name='kindeditor'),  # 增加kindeditor 富文本编辑器
    path('kindeditor_upload_img/', views.kindeditor_upload_img, name='kindeditor_upload_img'), # kindeditor 富文本编辑器 上传图片
]
