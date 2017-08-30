from django.shortcuts import render

# Create your views here.
from .models import Question
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from user.models import Userinfo

class Ask(CreateView):
    model=Question
    template_name = 'qa/ask.html'
    fields=['title','content','categories']
    
    def form_valid(self,form):
        form.instance.asker=self.request.user
        return super(Ask, self).form_valid(form)

class QuestionDetail(DetailView):
    """
    继承自DetailView，提供get_object函数（自动寻找并利用请求的url中携带的pk或slug参数，
    得到对应的模型对象），并默认寻求'<modelname>_detail.html'模板
    """
    model=Question

    def get_context_data(self, **kwargs):
        context=super(QuestionDetail,self).get_context_data(**kwargs)
        question=self.get_object()
        context['user']=question.asker
        return context

