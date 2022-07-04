from .models import UserProfile
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    uname = forms.CharField(label='用户名', max_length=24, error_messages={"min_length": "你太长了，最多24个字符", "required": "该字段不能为空!"})
    pword = forms.CharField(label='密码', min_length=6, error_messages={"min_length": "你太短了，需要6个字符", "required": "该字段不能为空!"})

    def clean_password(self):
        username = self.cleaned_data.get('uname')
        password = self.cleaned_data.get('pword')
        # print("username:",username,"password:",password)s
        print(self.cleaned_data)
        # if username == password:
        #     raise forms.ValidationError('密码不能与用户名一样！')
        return username,password


class RegisterForm(forms.ModelForm):
    """注册表单"""
    email = forms.EmailField(label='邮箱', min_length=3, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': '邮箱'}))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '密码'}))
    password1 = forms.CharField(label='再次输入密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '再次输入密码'}))

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean_email(self):
        """ 验证用户是否存在 """
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('邮箱已经存在!')
        return email

    def clean_password1(self):
        """验证密码是否相等"""
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise forms.ValidationError('两次密码输入不一致！')
        return self.cleaned_data['password1']


class ForgetPwdForm(forms.Form):
    """ 填写邮箱地址表单 """
    email = forms.EmailField(label='请输入注册邮箱地址', min_length=4, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': '用户名/邮箱'
    }))


class ModifyPwdForm(forms.Form):
    """Form definition for UserProfile."""
    password = forms.CharField(label='输入新密码', min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': '输入新密码'}))


class UserForm(forms.ModelForm):
    """ User模型的表单，只允许修改email一个数据，用户名不允许修改 """
    class Meta:
        model = User
        fields = ('email',)


class UserProfileForm(forms.ModelForm):
    """ UserProfile的表单 """
    class Meta:
        """Meta definition for UserInfoform."""
        model = UserProfile
        fields = ('nike_name', 'desc', 'gexing',
                  'birthday',  'gender', 'address', 'image')
