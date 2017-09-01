# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from user.models import Userinfo
from django.urls import reverse

class Question(models.Model):
    """
    问题表，所有属性默认非空

    asker：提问者， 外键，严格约束
    title：问题标题
    content：问题内容
    pubtime：发布时间，默认为当前时间
    categories：问题所属类别，可选多类，存为json字符串
    if_delete：该回答是否被删除，默认为0,删除后不显示给用户
    """
    asker = models.ForeignKey(Userinfo,on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    content = models.TextField()
    pubtime = models.DateTimeField(auto_now=True,blank=True)
    categories = models.TextField()
    if_delete = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('qa:question_detail',kwargs={'pk':self.pk})
    class Meta:
        db_table = 'question'


class Answer(models.Model):
    """
    回答表，所有属性默认非空

    question：对应问题的id,外键,保证完整性
    answer：回答者的id，外键，严格约束
    content：回答内容，不超过10000个字符
    pubtime：提交时间，默认为当前时间
    if_read：该回答是否已经被问题发布者读过，默认为0
    if_delete：该回答是否被删除，默认为0,删除后不显示给用户

    """
    question = models.ForeignKey(Question,on_delete=models.PROTECT)
    aswerer = models.ForeignKey(Userinfo,on_delete=models.PROTECT)
    content = models.CharField(max_length=10000)
    pubtime = models.DateTimeField(auto_now=True)
    if_read = models.IntegerField(default=0)
    if_delete = models.IntegerField(default=0)

    class Meta:
        db_table = 'answer'


class Comment(models.Model):
    """
    评论表，所有属性默认非空

    answer：所属答案id,外键，因为答案不可删，只是防止直接操作数据库删除，
            所以严格控制外键约束
    replier：评论者或者回复者id，外键，严格约束
    reply_to：回复对象id，评论时为评论发布者 ，当为回复时，表示目标对象，外键，严格约束
    content：回复内容
    pubtime：提交时间，默认为当前时间
    reply_in：当为回复时，允许为空，表示回复所属的评论
    if_read：是否被目标对象（当为评论时即为答案发布者）阅读过，默认为0
    if_delete：是否删除，默认为0,删除后不显示给用户

    """
    answer = models.ForeignKey(Answer,on_delete=models.PROTECT)
    replier = models.ForeignKey(Userinfo,on_delete=models.PROTECT,related_name='start_reply')
    reply_to = models.ForeignKey(Userinfo,on_delete=models.PROTECT,related_name='accept_reply')
    content = models.CharField(max_length=2000)
    pubtime = models.DateTimeField(auto_now=True)
    if_reply = models.IntegerField(default=0)
    reply_in = models.ForeignKey('self',on_delete=models.PROTECT,blank=True,null=True)
    if_read = models.IntegerField(default=0)
    if_delete = models.IntegerField(default=0)

    class Meta:
        db_table = 'comment'


class Invitation(models.Model):
    """
        邀请表，所有属性默认非空

        invited：邀请回答用户id，外键，严格约束
        question：问题id,外键，因为不可删，只是防止直接操作数据库删除，
                 所以严格控制外键约束
        state：邀请信息状态，未处理为0，已答为1，忽略为2，默认0
        content：邀请内容
        pubtime：提交时间，默认为当前时间
        if_delete：是否删除，默认为0,删除后不显示给用户

    """
    invited= models.ForeignKey(Userinfo,on_delete=models.PROTECT)
    question = models.ForeignKey(Question,on_delete=models.PROTECT)
    state = models.IntegerField(default=0)
    content=models.CharField(max_length=100)
    pubtime = models.DateTimeField(auto_now=True)
    if_delete = models.IntegerField(default=0)

    class Meta:
        db_table = 'invitation'


class Updown(models.Model):
    """
        点赞表，所有属性默认非空

        id：主键
        if_up：是否为点赞，0踩，1为点赞
        if_down：是否为回答，0为评论，1是
        ac_id：回答或评论的id，由于不确定类型，所以不能设置外键，由程序实现
        user：点赞用户的id，外键严格约束

    """
    id = models.BigIntegerField(primary_key=True)
    if_up = models.IntegerField()
    if_ans = models.IntegerField()
    ac_id = models.IntegerField()
    user = models.ForeignKey(Userinfo,on_delete=models.PROTECT)

    class Meta:
        db_table = 'updown'
