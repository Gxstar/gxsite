'''
表单
'''
from django import forms
from captcha.fields import CaptchaField


class CaptchaForm(forms.Form):
    '''
    定义验证码表单
    '''
    captcha = CaptchaField(label='验证码')
