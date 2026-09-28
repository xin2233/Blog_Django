"""users 应用的单元测试。

运行：
    python manage.py test users
    python manage.py test users.tests.MyBackendTests.test_login_with_email
"""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import EmailVerifyRecord


class LoginTests(TestCase):
    """MyBackend 支持用户名或邮箱登录。"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='zhangsan', email='zhangsan@example.com', password='pass12345')

    def _login(self, uname, pword):
        return self.client.post(reverse('users:login'), {'uname': uname, 'pword': pword})

    def test_login_with_username(self):
        resp = self._login('zhangsan', 'pass12345')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.id)

    def test_login_with_email(self):
        resp = self._login('zhangsan@example.com', 'pass12345')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.id)

    def test_login_with_wrong_password(self):
        resp = self._login('zhangsan', 'wrong-password')
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_picks_matching_account_when_email_is_duplicated(self):
        """邮箱不是唯一字段：同邮箱的多个账号中，应登录密码正确的那一个。"""
        other = User.objects.create_user(
            username='other', email='zhangsan@example.com', password='other12345')
        resp = self._login('zhangsan@example.com', 'other12345')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(int(self.client.session['_auth_user_id']), other.id)

    def test_login_redirects_to_index_when_already_logged_in(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('users:login'))
        self.assertRedirects(resp, reverse('blog:index'))


class ActiveUserTests(TestCase):
    """邮箱激活链接。"""

    def test_active_code_sets_is_staff(self):
        User.objects.create_user(username='a@example.com', email='a@example.com',
                                 password='pass12345')
        EmailVerifyRecord.objects.create(code='code123', email='a@example.com',
                                        send_type='register')
        resp = self.client.get(reverse('users:active_user', args=['code123']))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(User.objects.get(email='a@example.com').is_staff)

    def test_invalid_active_code_does_not_crash(self):
        resp = self.client.get(reverse('users:active_user', args=['nope']))
        self.assertEqual(resp.status_code, 200)


class PasswordResetTests(TestCase):
    """忘记密码链接。"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='a@example.com', email='a@example.com', password='old12345')
        cls.code = 'resetcode'
        EmailVerifyRecord.objects.create(code=cls.code, email='a@example.com',
                                        send_type='forget')

    def test_valid_code_resets_password(self):
        resp = self.client.post(reverse('users:forget_pwd_url', args=[self.code]),
                                {'password': 'new123456'})
        self.assertEqual(resp.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new123456'))

    def test_invalid_code_returns_message_instead_of_500(self):
        resp = self.client.post(reverse('users:forget_pwd_url', args=['badcode']),
                                {'password': 'new123456'})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '链接有误')
