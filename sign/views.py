from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
#def index(request):
#    return HttpResponse("Hello Django")

def index(request):
    return render(request, "index.html") #request 为请求对象，index.html 是返回给浏览器的HTML页面