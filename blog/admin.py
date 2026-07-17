from django.contrib import admin

# Register your models here.
from .models import Category, Post, Tag, Comment

admin.site.site_header = u"文章管理"
admin.site.site_title = u"文章管理"

admin.site.register(Category)
admin.site.register(Tag)


class PostAdmin(admin.ModelAdmin):
    """
    文章详情管理
    """

    list_display = ('id', 'title', 'category', 'tags', 'owner', 'pv', 'is_hot', 'pub_date',)
    list_filter = ('owner',)
    search_fields = ('title', 'desc')
    list_editable = ('is_hot',)
    list_display_links = ('id', 'title',)

    class Media:
        css = {
            'all': ('ckeditor5/cked.css',)
        }

        js = (
            'https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.js',
            'ckeditor5/ckeditor.js',
            'ckeditor5/translations/zh.js',
            'ckeditor5/config.js'
        )


admin.site.register(Post, PostAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """ 评论管理 """
    list_display = ('content_short', 'post', 'author_name', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at', 'post')
    search_fields = ('content', 'nickname', 'author__username')
    list_editable = ('is_approved',)
    list_display_links = ('content_short',)
    actions = ['approve_comments', 'disapprove_comments']

    @admin.display(description='评论内容')
    def content_short(self, obj):
        return obj.content[:50]

    @admin.display(description='评论者')
    def author_name(self, obj):
        return obj.nickname or obj.author.username if obj.author else '匿名'

    @admin.action(description='批量审核通过')
    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, '已审核通过 {} 条评论。'.format(updated))

    @admin.action(description='批量撤销审核')
    def disapprove_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, '已撤销 {} 条评论的审核。'.format(updated))
