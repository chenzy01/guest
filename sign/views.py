from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
#def index(request):
#    return HttpResponse("Hello Django")

def index(request):
    return render(request, "index.html") #request 为请求对象，index.html 是返回给浏览器的HTML页面

#登录函数
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username == 'admin' and password == 'admin123':
            return HttpResponseRedirect('/event_manage/')
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})

#发布会管理
def event_manage(request):
    return render(request, 'event_manage.html')