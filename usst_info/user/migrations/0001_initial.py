# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-20 09:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('st_num', models.CharField(max_length=10, unique=True)),
                ('passwd', models.CharField(max_length=500)),
                ('username', models.CharField(max_length=20)),
                ('under_graduate', models.IntegerField(default=1)),
                ('grade', models.CharField(max_length=4)),
                ('college', models.IntegerField(choices=[(1, '能源与动力工程学院'), (2, '光电信息与计算机工程学院'), (3, '管理学院'), (4, '机械学院'), (5, '外语学院'), (6, '环境与建筑学院'), (7, '医疗器械与食品学院'), (8, '出版印刷与艺术设计学院'), (9, '理学院'), (10, '中德学院'), (11, '中英国际学院'), (12, '材料科学与工程学院')])),
                ('major', models.IntegerField()),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('if_delete', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'userinfo',
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.IntegerField(default=0)),
                ('collect_id', models.IntegerField()),
                ('pubtime', models.DateTimeField(auto_now=True)),
                ('if_delete', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'collection',
            },
        ),
    ]
