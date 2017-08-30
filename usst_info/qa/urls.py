from django.conf.urls import url,include
from .views import Ask,QuestionDetail


app_name='qa'
urlpatterns=[
    url('^ask/$',Ask.as_view(),name='ask'),
    url('^detail/(?P<pk>\d{1,5})/$',QuestionDetail.as_view(),name='question_detail')
]
