# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Answer(models.Model):
    question_id = models.IntegerField()
    aswerer_id = models.IntegerField()
    content = models.CharField(max_length=10000)
    pubtime = models.DateTimeField()
    comments = models.IntegerField()
    up = models.IntegerField()
    down = models.IntegerField()
    if_read = models.IntegerField()
    if_delete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'answer'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Collection(models.Model):
    user_id = models.IntegerField()
    class_field = models.IntegerField(db_column='class')  # Field renamed because it was a Python reserved word.
    collect_id = models.IntegerField()
    pubtime = models.DateTimeField()
    if_delete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'collection'


class Comment(models.Model):
    answer_id = models.IntegerField()
    replier_id = models.IntegerField()
    content = models.CharField(max_length=2000)
    pubtime = models.DateTimeField()
    up = models.IntegerField()
    down = models.IntegerField()
    if_reply = models.IntegerField()
    reply_to_id = models.IntegerField(blank=True, null=True)
    reply_in_id = models.IntegerField(blank=True, null=True)
    if_read = models.IntegerField()
    if_delete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'comment'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Invitation(models.Model):
    invited_id = models.IntegerField()
    question_id = models.IntegerField()
    state = models.IntegerField()
    pubtime = models.DateTimeField()
    if_delete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'invitation'


class Jwcinfo(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    url = models.CharField(unique=True, max_length=200, blank=True, null=True)
    glances = models.IntegerField(blank=True, null=True)
    crawltime = models.DateTimeField()
    download = models.IntegerField()
    site = models.CharField(max_length=20)
    pubtime = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jwcinfo'


class PersonalInfo(models.Model):
    st = models.CharField(max_length=10)
    info = models.TextField()  # This field type is a guess.
    crawltime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'personal_info'


class Question(models.Model):
    asker_id = models.IntegerField()
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=10000)
    pubtime = models.DateTimeField()
    counts = models.IntegerField()
    class_field = models.TextField(db_column='class')  # Field renamed because it was a Python reserved word. This field type is a guess.
    if_delete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'question'


class Updown(models.Model):
    id = models.BigIntegerField(primary_key=True)
    if_up = models.IntegerField()
    if_down = models.IntegerField()
    ac_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'updown'


class Userinfo(models.Model):
    st_num = models.CharField(max_length=10)
    passwd = models.CharField(max_length=500)
    username = models.CharField(max_length=20)
    under_graduate = models.IntegerField()
    grade = models.CharField(max_length=4)
    college = models.IntegerField()
    major = models.IntegerField()
    email = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'userinfo'
