from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.views.generic.base import View
from django.views.generic import RedirectView
from django.contrib.auth.views import redirect_to_login
from django.conf import settings
import requests
class MyLoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        # 验证token
        print(request.COOKIES)
        authkey = request.COOKIES.get('authtoken', None)
        try:
            r = requests.get(f'{settings.SSO_CHECK_URL}{authkey}/', headers={'Connection':'close'}, timeout=settings.SSO_TIMEOUT).json()
            if r['code'] != 0:
                # 修改next
                callbackurl = 'http://centos7x04.test.com'+request.get_full_path()
                print(callbackurl)
                # 重新认证
                return redirect_to_login(callbackurl, self.get_login_url(), self.get_redirect_field_name())
        except requests.exceptions.ConnectTimeout:
            return JsonResponse({"msg": 'sso 认证超时', "code": 1})
        except Exception as e:
            return JsonResponse({"msg": 'sso error, {}'.format(str(e)), "code": 1})
        return super().dispatch(request, *args, **kwargs)


class IndexView(MyLoginRequiredMixin, View):

    def get(self, request):
        user = request.COOKIES.get('user', '')
        authtoken = request.COOKIES.get('authtoken')
        user_type = request.COOKIES.get('user_type', '')
        return render(request, 'index.html', locals())
        #return HttpResponse(f'welcome, {user_type}, {user}, you are surfing web3')


def logout(request, authtoken):
    try:
        r = requests.get(f'{settings.SSO_LOGOUT_URL}{authtoken}/', headers={'Connection':'close'}, timeout=settings.SSO_TIMEOUT).json()
        if r['code'] == 0:
            return redirect('login')
    except requests.exceptions.ConnectTimeout:
        return JsonResponse({"msg": 'sso接口超时', "code": 1})
    except Exception as e:
        return JsonResponse({"msg": 'sso error, {}'.format(str(e)), "code": 1})
