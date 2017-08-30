# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from user.models import Userinfo
from django.contrib.auth import authenticate

class MyBackend(object):

    def authenticate(self,st_num=None,passwd=None):
        """
        身份验证函数

        :param username: 用户的学号
        :param password: 学号对应的密码
        :return:
        """
        try:
            user = Userinfo.objects.get(st_num=st_num)
        except user.DoesNotExist:
            return None
        if user.check_passwd(passwd):
            return user
        return None

    def get_user(self, id):
        try:
            return Userinfo.objects.get(pk=id)
        except Userinfo.DoesNotExist:
            return None