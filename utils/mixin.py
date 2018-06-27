# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.forms import models as model_forms
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin as DjangoLoginRequiredMixin

from utils.base import is_token_valid


class CommonMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CommonMixin, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title or ''
        return context


class LoginRequiredMixin(DjangoLoginRequiredMixin):
    """ 重写，加入token过期时间判断 """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not check_token():
            pass
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class ModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class JsonFormMixin(object):
    """ json提交form表单的时候，返回json数据
    如果不需要request参数，设置类属性:
    form_no_request = True
    编辑删除区分:
    form_type = 'update'
    """
    form_no_request = False
    form_type = 'create'

    def get_form_kwargs(self):
        kwargs = super(JsonFormMixin, self).get_form_kwargs()
        if not self.form_no_request:
            kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):
        for label, err in form.errors.as_data().items():
            if len(err) > 0:
                err_str = '{}: {}'.format(label, err[0].message)
            return JsonResponse({'status': 1, 'msg': err_str})

    def form_valid(self, form):
        self.object = form.save()
        if not self.object:
            return JsonResponse({'status': 1, 'msg': "操作失败！"})

        return JsonResponse({'status': 0, 'msg': "操作成功！"})


class FieldClassMixin(object):
    """ 重写get_form_class
    主要用在不需要定义modelform的情况下，然后只要改field的class
    """
    def get_form_class(self):
        def _formfield_callback(f, **kwargs):
            f = f.formfield(**kwargs)
            f.widget.attrs['class'] = 'form-control'
            return f

        model = self.model
        return model_forms.modelform_factory(
            model, fields=self.fields, formfield_callback=_formfield_callback)
