from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

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
    #获取sessionid
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
    guest_list = Guest.objects.all()   #.order_by('id')

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
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html', {"user": username, "guests": contacts})

#嘉宾电话搜索
@login_required
def search_phone(request):
    #获取值为 user 的 Session 键值对，如果没有则返回空
    username = request.session.get('username', '')
    #获取参数 phone 的值（通过手机号输入框获取，点搜索后，url 会自动增加参数）
    search_phone = request.GET.get("phone", "")
    #search_phone_bytes = search_phone.encode(encoding="utf-8")
    guest_list = Guest.objects.filter(phone__contains=search_phone)

    paginator = Paginator(guest_list, 10)
    #当前要显示第几页数据
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # page 若不是整数，取第一页面数据
        contacts = paginator.page(1)
    except EmptyPage:
        #若 page 不在范围内，取最后一页面
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts, "pyhone": search_phone})

#签到页面
@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    guest_list = Guest.objects.filter(event_id=eid) #签到人数
    sign_list = Guest.objects.filter(sign="1", event_id=eid) #已签到人数
    guest_data = str(len(guest_list))
    sign_data = str(len(sign_list))
    return render(request, 'sign_index.html', {'event': event,
                                               'guest': guest_data,
                                               'sign': sign_data})


#签到功能
@login_required
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    guest_list = Guest.objects.filter(event_id=eid)
    guest_data = str(len(guest_list))
    sign_data = 0 #计算发布会已签到数量
    for guest in guest_list:
        if guest.sign == True:
            sign_data += 1

    phone = request.POST.get('phone', '')

    #将包含 phong 的手机号都查询出来
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'phone error.',
                                                   'guest': guest_data,
                                                   'sing': sign_data})

    #通过手机号和 发布会 id 进行查询
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'event id or phone error.',
                                                   'guest': guest_data,
                                                   'sing': sign_data})

    result = Guest.objects.get(phone=phone, event_id=eid)   #table.object.get() 获取返回的是一个对象
    if result.sign:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'user has sign in.',
                                                   'guest': guest_data,
                                                   'sing': sign_data})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'sign in success!',
                                                   'user': result,
                                                   'guest': guest_data,
                                                   'sign': str(int(sign_data)+1)})


#退出登录
@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response














