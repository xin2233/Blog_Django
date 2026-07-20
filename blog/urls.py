from django.urls import path, include

from . import views
from . import views_backend

app_name = "blog"

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>/', views.category_list, name='category_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('search/', views.search, name='search'),
    path('archives/<int:year>/<int:month>/', views.archives, name='archives'),
    path('comment/<int:post_id>/', views.submit_comment, name='submit_comment'),

    # 后台
    path('home_backend/', views_backend.home_backend, name='home_backend'),
    path('upload_img/', views_backend.uploadimg, name='upload_img'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('add_article/', views_backend.add_kindeditor, name='add_article'),
    path('edit_article/<int:post_id>/', views_backend.edit_kindeditor, name='edit_article'),
    path('delete_article/<int:post_id>/', views_backend.delete_article, name='delete_article'),
    path('toggle_article_status/<int:post_id>/', views_backend.toggle_article_status, name='toggle_article_status'),
    path('kindeditor_upload_img/', views_backend.kindeditor_upload_img, name='kindeditor_upload_img'),
    path('ajax_create_category/', views_backend.ajax_create_category, name='ajax_create_category'),
    path('ajax_create_tag/', views_backend.ajax_create_tag, name='ajax_create_tag'),
    path('category_tag_manager/', views_backend.category_tag_manager, name='category_tag_manager'),
    path('ajax_update_category/', views_backend.ajax_update_category, name='ajax_update_category'),
    path('ajax_delete_category/', views_backend.ajax_delete_category, name='ajax_delete_category'),
    path('ajax_update_tag/', views_backend.ajax_update_tag, name='ajax_update_tag'),
    path('ajax_delete_tag/', views_backend.ajax_delete_tag, name='ajax_delete_tag'),
    path('backup_restore/', views_backend.backup_restore, name='backup_restore'),
]
