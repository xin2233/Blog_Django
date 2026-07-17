from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from secrets import choice
import string

# 这个方法返回一个8位数的随机字符串

def random_str(randomlength=8):
    # 生成a-z,A-Z,0-9左右的字符
    chars = string.ascii_letters + string.digits
    # 从a-zA-Z0-9生成指定数量的随机字符
    strcode = ''.join(choice(chars) for _ in range(randomlength))
    return strcode

def send_register_email(email, send_type='register'):
    code = random_str()
    if send_type == 'register':
        email_title = '博客的注册激活链接'
        email_body = '请点击下面链接激活你的账号：http://127.0.0.1:8000/users/active/{0}'.format(code)
    elif send_type == 'forget':
        email_title = '博客密码重置链接'
        email_body = '请点击以下链接修改密码：http://127.0.0.1:8000/users/forget_pwd_url/{0}'.format(code)
    else:
        raise ValueError('Unsupported email type.')

    with transaction.atomic():
        send_status = send_mail(email_title, email_body, settings.DEFAULT_FROM_EMAIL, [email])
        if not send_status:
            return False
        EmailVerifyRecord.objects.create(code=code, email=email, send_type=send_type)
    return True
