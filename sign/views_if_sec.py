from django.contrib import auth as django_auth
import base64
from django.core.exceptions import ObjectDoesNotExist
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


def add_event(request):
    pass


def get_guest_list(request):
    pass
