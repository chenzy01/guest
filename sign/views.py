from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from sign.models import Event, Guest

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
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user) #登录
            #response.set_cookie('user', username, 3600) #添加浏览器的cookie
            request.session['user'] = username #将session信息记录到服务器
            response = HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})

#发布会管理
@login_required
def event_manage(request):
    #username = request.COOKIES.get('user', '') #读取浏览器cookie
    event_list = Event.objects.all()
    username = request.session.get('user', '') #读取浏览器的session
    return render(request, 'event_manage.html', {"user": username, "events": event_list})

#发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username, "events": event_list})

#嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    return render(request, 'guest_manage.html', {"user":username, "guests": guest_list})

#嘉宾电话搜索
@login_required
def search_phone(request):
    username = request.session.get('user', '')
    search_phone = request.GET.get("phone", "")
    guest_list = Guest.objects.filter(phone__contains=search_phone)
    return render(request, "guest_manage.html", {"user": username, "guests": guest_list})
















