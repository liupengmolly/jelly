from django.shortcuts import render

# Create your views here.


def index(request):
    """
    网站的首页，无需登录即可进入，可以搜索、登录、注册、进入用户中心、查看推荐信息等

    :param request:
    :return:
    """
    return render(request,'index.html')