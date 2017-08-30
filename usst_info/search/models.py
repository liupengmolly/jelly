# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Jwcinfo(models.Model):
    """
       爬取的学校公共信息表，所有属性默认非空

       title：标题，允许为空
       body：正文，允许为空
       url：所属通知链接，允许为空
       glances：通知在本网站被点击浏览的次数，默认为0
       crawltime：爬取时间，默认当前时间
       download：是否包含下载，默认为0，不包含
       site：通知来源网站
       pubtime：通知在来源网站的发布时间，允许为空
    """
    title = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    url = models.CharField(unique=True, max_length=200, blank=True, null=True)
    glances = models.IntegerField(default=0)
    crawltime = models.DateTimeField(auto_now=True)
    download = models.IntegerField(default=0)
    site = models.CharField(max_length=20)
    pubtime = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'jwcinfo'


class PersonalInfo(models.Model):
    """
       爬取的用户在学校的个人信息表，所有属性默认非空

       st：学生的学号，为了方便，没有使用学生表对应的id，所以需要有程序保证引用完整性，唯一
       info：学生信息的json字符串
       crawltime：爬取时间，默认为爬取的当前时间
    """
    st = models.CharField(max_length=10,unique=True)
    info = models.TextField()
    crawltime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'personal_info'
