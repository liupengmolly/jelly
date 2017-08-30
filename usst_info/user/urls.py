from django.conf.urls import url,include
from user import views

app_name='user'
urlpatterns=[
    url(r'^$',views.auth,name='auth'),
    url(r'^signin/$',views.signin,name='signin'),
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^find_passwd/$',views.find_passwd,name='find_passwd'),
    url(r'^user_info/(?P<user_id>\d{1,5})/$',views.user_info,name='user_info'),
    url(r'^personal_info/$',views.personal_info,name='personal_info')
]
