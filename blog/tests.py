"""blog 应用的单元测试。

运行：
    python manage.py test blog
    python manage.py test blog.tests.PostVisibilityTests.test_draft_detail_returns_404
"""
import os
import tarfile
import tempfile
from unittest import mock

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings

from .models import Category, Comment, Post, Tag


class BlogTestCase(TestCase):
    """提供文章/分类/标签的公共数据。"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='author', password='pass12345')
        cls.category = Category.objects.create(name='Python')
        cls.tag = Tag.objects.create(name='django')
        cls.published = Post.objects.create(
            title='已发布文章', content='已发布正文', category=cls.category,
            owner=cls.user, tags=cls.tag, status='published')
        cls.draft = Post.objects.create(
            title='草稿文章', content='草稿正文', category=cls.category,
            owner=cls.user, tags=cls.tag, status='draft')


class PostVisibilityTests(BlogTestCase):
    """草稿只能在后台看到，前台任何入口都不应泄露。"""

    def test_index_only_shows_published(self):
        resp = self.client.get('/')
        self.assertContains(resp, '已发布文章')
        self.assertNotContains(resp, '草稿文章')

    def test_category_list_only_shows_published(self):
        resp = self.client.get('/category/{}/'.format(self.category.id))
        self.assertContains(resp, '已发布文章')
        self.assertNotContains(resp, '草稿文章')

    def test_search_does_not_leak_draft(self):
        resp = self.client.get('/search/', {'keyword': '草稿'})
        self.assertNotContains(resp, '草稿文章')

    def test_archives_only_shows_published(self):
        resp = self.client.get('/archives/{}/{}/'.format(
            self.published.add_date.year, self.published.add_date.month))
        self.assertContains(resp, '已发布文章')
        self.assertNotContains(resp, '草稿文章')

    def test_draft_detail_returns_404(self):
        resp = self.client.get('/post/{}/'.format(self.draft.id))
        self.assertEqual(resp.status_code, 404)

    def test_prev_next_post_skips_draft(self):
        # 造一篇 id 更大的草稿，确保它不会被当成「下一篇」
        Post.objects.create(title='更晚的草稿', content='x', category=self.category,
                            owner=self.user, status='draft')
        resp = self.client.get('/post/{}/'.format(self.published.id))
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, '草稿文章')
        self.assertNotContains(resp, '更晚的草稿')

    def test_pagination_two_per_page(self):
        for i in range(3):
            Post.objects.create(title='分页文章{}'.format(i), content='x',
                                category=self.category, owner=self.user, status='published')
        resp = self.client.get('/')
        page = resp.context['page_obj']
        self.assertEqual(page.paginator.count, 4)      # 1 篇已发布 + 3 篇新增，草稿不计
        self.assertEqual(page.paginator.num_pages, 2)  # 每页 2 篇


class CommentTests(BlogTestCase):
    """评论需要审核，回复挂在父评论下。"""

    def test_unapproved_comment_is_hidden(self):
        comment = Comment.objects.create(post=self.published, content='未审核评论')
        resp = self.client.get('/post/{}/'.format(self.published.id))
        self.assertNotContains(resp, '未审核评论')

        comment.is_approved = True
        comment.save()
        resp = self.client.get('/post/{}/'.format(self.published.id))
        self.assertContains(resp, '未审核评论')

    def test_reply_is_nested_under_parent(self):
        parent = Comment.objects.create(post=self.published, content='父评论', is_approved=True)
        Comment.objects.create(post=self.published, content='子回复',
                               parent=parent, is_approved=True)
        resp = self.client.get('/post/{}/'.format(self.published.id))
        self.assertContains(resp, '父评论')
        self.assertContains(resp, '子回复')
        # 子回复不作为顶级评论重复出现
        self.assertEqual(len(resp.context['comments']), 1)

    def test_submit_comment_waits_for_approval(self):
        self.client.post('/comment/{}/'.format(self.published.id), {'content': '新评论'})
        comment = Comment.objects.get(content='新评论')
        self.assertFalse(comment.is_approved)
        resp = self.client.get('/post/{}/'.format(self.published.id))
        self.assertNotContains(resp, '新评论')

    def test_submit_empty_comment_is_rejected(self):
        self.client.post('/comment/{}/'.format(self.published.id), {'content': '   '})
        self.assertFalse(Comment.objects.exists())

    def test_submit_reply_attaches_parent(self):
        parent = Comment.objects.create(post=self.published, content='父评论', is_approved=True)
        self.client.post('/comment/{}/'.format(self.published.id),
                         {'content': '我的回复', 'parent_id': parent.id})
        self.assertEqual(Comment.objects.get(content='我的回复').parent, parent)


class BackupCommandTests(TestCase):
    """manage.py backup — 只验证打包结果，不做破坏性操作。"""

    def test_backup_contains_data_and_media(self):
        with tempfile.TemporaryDirectory() as tmp:
            media_root = os.path.join(tmp, 'media')
            os.makedirs(os.path.join(media_root, 'upload/img'))
            with open(os.path.join(media_root, 'upload/img/a.png'), 'wb') as f:
                f.write(b'fake png')
            output = os.path.join(tmp, 'backup.tar.gz')
            with override_settings(MEDIA_ROOT=media_root):
                call_command('backup', output, verbosity=0)

            self.assertTrue(os.path.exists(output))
            with tarfile.open(output) as tar:
                names = tar.getnames()
            self.assertIn('data.json', names)
            self.assertTrue(any(n.startswith('media') for n in names))


class RestoreCommandTests(TestCase):
    """manage.py restore — 只覆盖不会真正 flush 数据库的分支。"""

    def _make_tarball(self, tmp, members=('data.json',)):
        path = os.path.join(tmp, 'x.tar.gz')
        with tarfile.open(path, 'w:gz') as tar:
            for name in members:
                fpath = os.path.join(tmp, name)
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write('[]')
                tar.add(fpath, arcname=name)
        return path

    def test_missing_file_raises(self):
        with self.assertRaises(CommandError):
            call_command('restore', '/tmp/definitely-not-exists.tar.gz', verbosity=0)

    def test_non_tarball_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, 'x.tar.gz')
            with open(path, 'wb') as f:
                f.write(b'not a tarball')
            with self.assertRaises(CommandError):
                call_command('restore', path, verbosity=0)

    def test_tarball_without_data_json_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._make_tarball(tmp, members=('readme.txt',))
            with mock.patch('builtins.input', return_value='yes'):
                with self.assertRaises(CommandError):
                    call_command('restore', path, verbosity=0)

    def test_user_can_abort_before_flush(self):
        user = User.objects.create_user(username='keepme', password='pass12345')
        with tempfile.TemporaryDirectory() as tmp:
            path = self._make_tarball(tmp)
            with mock.patch('builtins.input', return_value='no'):
                call_command('restore', path, verbosity=0)
        self.assertTrue(User.objects.filter(id=user.id).exists())
