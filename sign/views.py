from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    username = request.session.get('username', '')
    guest_list = Guest.objects.all().order_by('id')

    paginator = Paginator(guest_list, 2)
    # get 请求获取当前要显示第几页数据
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        #page 若不是整数，取第一页面数据
        contacts = paginator.page(1)
    except EmptyPage:
        #若 page 不在范围内，取最后一页面
        page = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html', {"user":username, "guests": contacts})

#嘉宾电话搜索
@login_required
def search_phone(request):
    #获取值为 user 的 Session 键值对，如果没有则返回空
    username = request.session.get('username', '')
    #获取参数 phone 的值（通过手机号输入框获取，点搜索后，url 会自动增加参数）
    search_phone = request.GET.get("phone", "")
    search_phone_bytes = search_phone.encode(encoding='utf-8')
    guest_list = Guest.objects.filter(phone__contains=search_phone_bytes)

    paginator = Paginator(guest_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # page 若不是整数，取第一页面数据
        contacts = paginator.page(1)
    except EmptyPage:
        #若 page 不在范围内，取最后一页面
        page = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts, "pyhone":search_phone})
















