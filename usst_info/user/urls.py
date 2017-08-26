from django.conf.urls import url,include
from user import views

urlpatterns=[
    url(r'^$',views.auth),
    url(r'^signin/$',views.signin),
    url(r'^signup/$',views.signup),
    url(r'^find_passwd/$',views.find_passwd),
]