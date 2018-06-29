#!/usr/bin/env python
# coding: utf-8 
# @Time   : forms.py
from django import forms
from django.contrib import auth



class LoginForm(forms.Form):
    username = forms.CharField(max_length=36, required=True, error_messages={'required': '用户名不能为空','max_length': '用户名长度不能大于36'})
    password = forms.CharField(max_length=50, strip=False, widget=forms.PasswordInput, required=True, error_messages={'required': '密码不能为空','max_length': '密码长度不能大于36'})

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)


    def clean_username(self):
        # 在field.clean()后执行该方法
        username = self.cleaned_data['username']
        print('username')
        print(self.cleaned_data)
        return username

    def clean_password(self):
        # 在field.clean()后执行该方法
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        print("password")
        print(self.cleaned_data)
        if username and password:
            self.user_cache = auth.authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(u'账号密码不匹配')
            elif not self.user_cache.is_active:
                raise forms.ValidationError(u'此账号已被禁用')

        print(self.cleaned_data)
        return password

    def get_user(self):
        return self.user_cache

