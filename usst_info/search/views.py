# -*- encoding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import SESSION_KEY
from user.models import Userinfo
# Create your views here.


def index(request):
    """
    网站的首页，无需登录即可进入，可以搜索、登录、注册、进入用户中心、查看推荐信息等

    :param request:
    :return:
    """
    user=Userinfo.objects.get(pk=request.session[SESSION_KEY])
    if user:
        info={'url':'/user/personal_info','name':user.username}
    else:
        info={'url':'/user','name':'登录/注册'}
    return render(request,'index.html',info)
