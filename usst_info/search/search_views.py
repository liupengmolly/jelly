# -*- coding:utf-8 -*-
from haystack.views import SearchView
from .models import Jwcinfo,Userinfo
from haystack.query import SearchQuerySet,EmptySearchQuerySet,ValuesSearchQuerySet
from haystack.inputs import Raw
import math
from django.utils.encoding import force_text, python_2_unicode_compatible
import re
from haystack.inputs import Clean,Exact,Not,BaseInput
import datetime

class MySearchView(SearchView):
    mysearchqueryset=SearchQuerySet()
    user=None

    def get_results(self):
        if not self.form.is_valid():
            return EmptySearchQuerySet()
        if not self.form.cleaned_data.get('q'):
            return EmptySearchQuerySet()
        #加重含学生学院字段的通知的权重
        if self.request.session.get('stu_num',False):
            num = self.request.session['stu_num']
            self.user = Userinfo.objects.get(stu_num=num)
            recom=self.mysearchqueryset.boost(self.user.college,1.2)\
                .auto_query(self.form.cleaned_data['q']).order_by('-pubtime','-glances','-download')
        else:
            recom=1
            #先对title字段的搜索匹配效果加成，然后执行检索，再按发布时间、浏览量排序
        sqs=self.mysearchqueryset.auto_query(self.form.cleaned_data['q'])\
            .order_by('-pubtime','-glances','-download')
        if recom!= 1:
            sqs=recom[0:1]+sqs[1:3]+recom[1:2]+sqs[3:5]+recom[2:3]+sqs[5:]
        return sqs

    def extra_context(self):
        """get shortcut of articles,
         10 in 1 page."""
        #取最新发布、最近最多浏览、教务处最新发布以及以学生学院进行查询所得的最相关组合推荐
        most_recent=self.mysearchqueryset.exclude(pubtime='2111-11-11').order_by('-pubtime')[:20]
        most_browse=self.mysearchqueryset.filter(pubtime__gte=(datetime.datetime.now()\
                    +datetime.timedelta(-7))).order_by('-glances')[:10]
        most_recent_jwc= self.mysearchqueryset.filter(site='教务处').exclude(pubtime='2111-11-11').order_by('-pubtime')
        context = super(MySearchView, self).extra_context()
        if self.request.session.get('stu_num', False):
            num = self.request.session['stu_num']
            self.user = Userinfo.objects.get(stu_num=num)
            most_relevant = self.mysearchqueryset.auto_query(self.user.college).order_by('-pubtime', 'glances')
            context['side_list'] =set(most_browse[0:2]+most_relevant[0:2]+most_recent_jwc[0:1]+most_recent[0:1])
            context['title']="Jelly为"+self.user.username+"推荐"
        else:
            context['side_list'] = set(most_browse[0:2]+most_recent[0:2]+most_recent_jwc[0:2])
            context['title']="Jelly推荐"
        return context
