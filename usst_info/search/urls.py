from django.conf.urls import url,include
from search import views
from search import search_views

urlpatterns=[
    url(r'^$',search_views.MySearchView(),name='haystack_search')
]
