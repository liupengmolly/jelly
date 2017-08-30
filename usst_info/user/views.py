# -*- encoding:utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from user.models import Userinfo,UserManager
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,SESSION_KEY
from usst_info.settings import colleges,majors
# Create your views here.


def auth(request):
    """
    网站的首页，无需登录即可进入，可以搜索、登录、注册、进入用户中心、查看推荐信息等

    :param request:
    :return:
    """
    return render(request,'user/auth.html')

@csrf_protect
def signin(request):
    """
    登录验证
    login函数使用django默认的函数，包括身份验证模块

    :param request:
    :return:
    """
    st_num=request.POST['signin_ac']
    passwd=request.POST['signin_pwd']
    user=authenticate(st_num=st_num,passwd=passwd)
    if user:
        login(request,user)
        return render(request,'index.html',{'url':'/user/personal_info','name':user.username})
    else:
        return render(request,'404.html')

@csrf_protect
def signup(request):
    """
    注册

    :param request:
    :return:
    """
    st_num=request.POST['signup_ac']
    password=request.POST['signup_pwd']
    username=request.POST['signup_name']
    email=request.POST['signup_email']
    under_graduate=request.POST['signup_degree']
    grade=request.POST['signup_grade']
    college=request.POST['signup_college']
    major=request.POST['signup_major']
    usermanager=UserManager()
    user=usermanager.create_user(st_num,password,username,email,under_graduate,grade,college,major)
    return render(request,'user/auth.html')

def user_info(request,user_id):
    """
    用户详情页
    :param request:
    :param user_id:
    :return:
    """
    user=Userinfo.objects.get(pk=user_id)
    degree = '本科生' if user.under_graduate else '研究生'
    role = '管理员' if user.is_admin else ''
    college = colleges[user.college]
    major = majors[user.college][user.major]
    return render(request,'user/user_info.html',{'user':user,'degree':degree, 'role':role,
                                            'college':college,'major':major})

def personal_info(request):
    """
    用户个人中心
    由于用户模型的很多信息不是直接存储的字符串信息，所以需要转换
    :param request:
    :return:
    """
    user=Userinfo.objects.get(pk=request.session[SESSION_KEY])
    degree='本科生' if user.under_graduate else '研究生'
    role='管理员' if user.is_admin else ''
    college=colleges[user.college]
    major=majors[user.college][user.major]

    return render(request, 'user/personal_info.html', {'degree':degree, 'role':role,
                                            'college':college,'major':major})

def find_passwd(request):
    return render(request,'user/find_passwd.html')
