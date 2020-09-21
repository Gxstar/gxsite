'''
表单
'''
from django import forms
from captcha.fields import CaptchaField


class CaptchaForm(forms.Form):
    '''
    定义验证码表单
    '''
    username = forms.CharField(required=True, label='用户名', max_length=12, widget=forms.TextInput({
        'placeholder': '用户名',
    }))
    email = forms.EmailField(required=True, label='邮箱',widget=forms.EmailInput({
        'placeholder': '邮箱地址',
    }))
    body = forms.CharField(required=True, label='评论', widget=forms.Textarea({
        'placeholder': '评论',
        'rows':'5',
        'style':'width:100%',
    }))
    captcha = CaptchaField(required=True, label='验证码')
