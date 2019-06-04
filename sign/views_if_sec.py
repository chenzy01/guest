import base64
import hashlib
import time

from django.contrib import auth as django_auth
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import JsonResponse

from guest.sign.models import Event

"""
为接口参加安全机制：认证、签名、AES加密
"""

# 用户验证


def user_auth(request):
    """
    request.META 包含本次 HTTP 请求的 Header 信息
    HTTP_AUTHORIZATION ,用于获取 HTTP 认证数据
    """
    get_http_auth = request.META.get('HTTP_AUTHORIZATION', b'')
    auth = get_http_auth.split()
    try:
        # base64 对加密的字符串进行解码
        auth_parts = base64.b64decode(auth[1]).decode('utf-8').partition(':')
    except IndexError:
        return "null"

    username, password = auth_parts[0], auth_parts[2]
    user = django_auth.authenticate(username=username, password=password)
    if user is not None:
        # 调用认证模块，对得到的 auth 进行验证
        django_auth.login(request, user)
        return "success"
    else:
        return "fail"


# 查询发布会接口--增加用户验证
def get_event_list(request):
    auth_result = user_auth(request)  # 调用认证函数
    if auth_result == "null":
        return JsonResponse({'status': 10011, 'message': 'user auth null'})

    if auth_result == "fail":
        return JsonResponse({'status': 10012, 'message': 'user auth fail'})

    eid = request.GET.get("eid", "")  # 发布会id
    name = request.GET.get("name", "")  # 发布会名称

    if eid == '' and name == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'message': 'query result in empty'})
        else:
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({'status': 200, 'message': 'success', 'data': event})

    if name != '':
        datas = {}
        results = Event.objects.get(name_contains=name)
        if results:
            for re in results:
                event = {'eid': re.id, 'name': re.name, 'limit': re.limit, 'status': re.status, 'address': re.address,
                         'start_time': re.start_time}
                datas.append(event)
            return JsonResponse({'status': 200, 'datas': datas})
    else:
        return JsonResponse({'status': 10022, 'message': 'query in empty'})


# 用户签名+时间戳
def user_sign(request):
    if request.method == 'POST':
        client_time = request.POST.get('time', '')  # 客户端时间戳
        client_sign = request.POST.get('sign', '')  # 客户端签名
    else:
        return "error"

    if client_time == '' or client_sign == '':
        return "sign null"

    # 服务器时间戳
    now_time = time.time()
    # 将时间戳转化为字符串类型，并截取小数点前的时间
    server_tiem = str(now_time).split('.')[0]
    # 获取时间差
    time_difference = int(server_tiem) - int(client_time)
    if time_difference >= 60:
        return "timeout"

    # 签名检查
    md5 = hashlib.md5()
    # 密钥字符串：&Guest-Bugmaster
    sign_str = client_time + "&Guest-Bugmaster"
    sign_bytes_utf8 = sign_str.encode(encoding="utf-8")
    md5.update(sign_bytes_utf8)
    server_sign = md5.hexdigest()

    if server_sign != client_sign:
        return "sign fail"
    else:
        return "sign success"


# 添加发布会接口，增加签名+时间戳
def add_event(request):
    sign_result = user_sign(request)
    if sign_result == "error":
        return JsonResponse({'status': 10011, 'message': 'request error'})
    elif sign_result == "sign null":
        return JsonResponse({'status': 10012, 'message': 'user sign null'})
    elif sign_result == "timeout":
        return JsonResponse({'status': 10013, 'message': 'user sign timeout'})
    elif sign_result == "sign fail":
        return JsonResponse({'status': 10014, 'message': 'user sign error'})

    eid = request.POST.get('eid', '')
    name = request.POST.get('name', '')
    limit = request.POST.get('limit', '')
    status = request.POST.get('status', '')
    address = request.POST.get('address', '')
    start_time = request.POST.get('start_time', '')

    if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status': 10022, 'message': 'event id already exists'})

    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status': 10023, 'message': 'event name already exists'})

    if status == '':
        status = 1

    try:
        Event.objects.create(id=eid, name=name, limit=limit, address=address, status=int(status), start_time=start_time)
    except ValidationError:
        error = 'start_time format error. It must be in YYYY-MM-DD HH:MM:SS format.'
        return JsonResponse({'status': 10024, 'message': error})

    return JsonResponse({'status': 200, 'message': 'add event success'})





