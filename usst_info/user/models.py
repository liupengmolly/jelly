# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

import hashlib
from django.db import models
from django.contrib.auth.hashers import check_password,is_password_usable,make_password
from django.contrib.auth.base_user import BaseUserManager
from django.utils.crypto import salted_hmac
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, st_num,passwd,username, email,under_graduate, grade, college, major, **extra_fields):
        """
        Creates and saves a User with the given username, email and passwd.
        """
        email = self.normalize_email(email)
        user = Userinfo(
            st_num=st_num,
            username=username,
            email=email,
            under_graduate=under_graduate,
            grade=grade,
            college=college,
            major=major,
            **extra_fields)
        user.set_passwd(passwd)
        user.save(using=self._db)
        return user

    def create_user(self, st_num,passwd,username, email,under_graduate, grade, college, major, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('if_delete',False)
        return self._create_user(st_num,passwd,username, email,under_graduate, grade, college, major, **extra_fields)

    def create_superuser(self, st_num,passwd,username, email,under_graduate, grade, college, major, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('if_delete', False)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(st_num,passwd,username, email,under_graduate, grade, college, major, **extra_fields)


class Userinfo(models.Model):
    """
    用户个人信息表，所有属性默认非空

    直接用类对数据库操作时一般格式是：class.objects.method()，在此基础上建立
    基于有一定业务逻辑实例化对象的函数，用self.method()直接引用

    st_num：学号
    passwd：密码（教务系统对应的密码）
    username：用户名
    undergraduate：是否是本科生，默认为1（是）,0表示硕士生
    grade：年级，以入学年份代表
    college：学院，choices为COLLEGES
    major：系或专业
    email：邮箱，保证唯一性
    is_delete：用户是否已经被有效，默认为False，删除用户置为True
    is_admin：是否为管理员账户
    """
    COLLEGES=(
        (1,'能源与动力工程学院'),
        (2,'光电信息与计算机工程学院'),
        (3,'管理学院'),
        (4,'机械学院'),
        (5,'外语学院'),
        (6,'环境与建筑学院'),
        (7,'医疗器械与食品学院'),
        (8,'出版印刷与艺术设计学院'),
        (9,'理学院'),
        (10,'中德学院'),
        (11,'中英国际学院'),
        (12,'材料科学与工程学院'),
    )
    # ND_COLLEGE=(
    #     (0,'未分专业'),
    #     (1,'过程装备与控制工程'),
    #     (2,'新能源科学与工程'),
    #     (3,'能源与动力工程'),
    # )
    # GD_COLLEGE=(
    #     (0, '未分专业'),
    #     (1,'测控技术与仪器'),
    #     (2,'电子信息工程'),
    #     (3,'通信工程'),
    #     (4,'电子科学与技术'),
    #     (5,'智能科学与技术'),
    #     (6,'计算机科学与技术'),
    #     (7,'网络工程'),
    #     (8,'电气工程及其自动化'),
    #     (9,'自动化'),
    #     (10,'光电信息科学与工程'),
    #     (11,'光电信息科学与工程（中德合作）'),
    # )
    # GL_COLLEGE=(
    #     (0, '未分专业'),
    #     (1, '国际经济与贸易'),
    #     (2, '金融学'),
    #     (3, '管理科学'),
    #     (4, '信息管理与信息系统'),
    #     (5, '工业工程'),
    #     (6, '工商管理（中美合作）'),
    #     (7, '会计学'),
    #     (8, '公共事业管理'),
    #     (9, '公共事业管理（体育）'),
    #     (10, '税收学'),
    # )
    # JX_COLLEGE=(
    #     (0, '未分专业'),
    #     (1, '机械设计制造及其自动化'),
    #     (2, '车辆工程'),
    #     (3, '机械设计制造及其自动化（国际工程）（中德合作）'),
    # )
    # WY_COLLEGE=(
    #     (0, '未分专业'),
    #     (1, '英语'),
    #     (2, '德语'),
    #     (3, '日语'),
    #     (4, '英语（中美合作）'),
    # )
    # HJ_COLLEGE=(
    #     (0, '未分专业'),
    #     (1, '土木工程'),
    #     (2, '环境工程'),
    #     (3, '建筑环境与能源应用工程'),
    # )
    # YS_COLLEGE=(
    #     (0, '未分专业'),
    #     (1, '生物医学工程'),
    #     (2, '食品科学与工程'),
    #     (3, '食品质量与安全'),
    #     (4, '医学影像技术'),
    #     (5, '医学信息工程'),
    #     (6, '制药工程'),
    #     (7, '假肢矫形工程'),
    # )
    # BY_COLLEGE=(
    #     (0, '未分专业'),
    #     (1, '广告学'),
    #     (2, '编辑出版学'),
    #     (3, '传播学'),
    #     (4, '包装工程'),
    #     (5, '工业设计'),
    #     (6, '动画'),
    #     (7, '视觉传达设计'),
    #     (8, '产品设计'),
    #     (9, '环境设计'),
    #     (10, '印刷工程（卓越班）'),
    # )
    # L_COLLEGE=(
    #     (0, '未分专业'),
    #     (1, '数学与应用数学'),
    #     (2, '应用物理学'),
    #     (3, '应用化学'),
    # )
    # ZD_COLLEGE=(
    #     (0, '未分专业'),
    #     (1, '电气工程及其自动化（中德合作）'),
    # )
    # ZY_COLLEGE=(
    #     (0, '未分专业'),
    #     (1, '电子信息科学与技术'),
    #     (2, '机械设计及其自动化（中英合作）'),
    #     (3, '会展经济与管理（中英合作）'),
    #     (4, '工商管理'),
    # )
    # CL_COLLEGE=(
    #     (0, '未分专业'),
    #     (1, '材料科学与工程'),
    #     (2, '材料科学与工程（卓越班）'),
    #     (3, '材料成型及控制工程'),
    # )
    st_num = models.CharField(max_length=10,unique=True)
    passwd = models.CharField(max_length=500)
    username = models.CharField(max_length=20)
    under_graduate = models.IntegerField(default=1)
    grade = models.CharField(max_length=4)
    college = models.IntegerField(choices=COLLEGES)
    major = models.IntegerField()
    email = models.EmailField(max_length=50,unique=True)
    last_login=models.DateTimeField(_('last login'),blank=True,null=True)
    if_delete=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)

    USERNAME_FIELD='st_num'
    REQUIRED_FIELDS=['email']#在创建超级用户时需要的

    objects=UserManager()

    def __str__(self):
        return self.st_num+':'+self.username

    def get_user(self, id):
        try:
            return self.objects.get(pk=id)
        except self.DoesNotExist:
            return None

    def get_user_by_st_num(self,st_num):
        try:
            return Userinfo.objects.get(st_num=st_num)
        except Userinfo.DoesNotExist:
            return None

    def set_passwd(self, raw_passwd):
        self.passwd = make_password(raw_passwd)
        self._passwd = raw_passwd

    def check_passwd(self, raw_passwd):
        """
        Return a boolean of whether the raw_passwd was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_passwd):
            self.set_passwd(raw_passwd)
            # passwd hash upgrades shouldn't be considered passwd changes.
            self._passwd = None
            self.save(update_fields=["password"])
        return check_password(raw_passwd, self.passwd, setter)

    def set_unusable_passwd(self):
        # Set a value that will never be a valid hash
        self.passwd = make_password(None)

    def has_usable_passwd(self):
        return is_password_usable(self.passwd)

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.passwd).hexdigest()


    @property
    def is_anonymous(self):
        return False if self.st_num is not None else True

    @property
    def is_authenticated(self):
        return True if self.st_num is not None else False

    class Meta:
        db_table = 'userinfo'


class Collection(models.Model):
    """
    收藏表，所有属性默认非空

    user：收藏者的id，外键，严格约束
    category：收藏的信息种类，0表示校园公共信息，1,表示校园个人信息2表示问题，3表示答案，默认为0
    collecte_id：收藏的信息id，因为信息类型不固定，所以不能设置外键，需由程序实现
    pubtime：收藏时间，默认当前时间
    if_delete：是否已经取消收藏，默认为0，如果取消（1）,将不再显示该收藏
    """
    user = models.ForeignKey(Userinfo,on_delete=models.PROTECT)
    category = models.IntegerField(default=0)
    collect_id = models.IntegerField()
    pubtime = models.DateTimeField(auto_now=True)
    if_delete = models.IntegerField(default=0)

    class Meta:
        db_table = 'collection'
