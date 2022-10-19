from django.forms import forms


class EmpForm(forms.Form):
    catetory = forms.CheckboxInput('1', '2', '3')

    def clean_catetory(self):  # 局部狗子
        pass

    def clean(self):  # 全局钩子
        pass
