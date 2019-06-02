from django.urls import path
from guest.sign import views_if
from guest.sign import views_if_sec

app_name = "sign"

urlpatterns = [
    # sign system interface:
    # ex : /api/add_event/
    path('add_event/', views_if.add_event, name='add_event'),
    # ex : /api/add_guest/
    path('add_guest/', views_if.add_guest, name='add_guest'),
    # ex : /api/get_event_list/
    path('get_event_list/', views_if.get_event_list, name='get_event_list'),
    # ex : /api/get_guest_list/
    path('get_guest_list/', views_if.get_guest_list, name='get_guest_list'),
    # ex : /api/user_sign/
    path('user_sign/', views_if.user_sign, name='user_sign'),

    # security interface
    # ex : /api/sec_get_event_list/
    path('sec_get_event_list/', views_if_sec.get_event_list, name='get_event_list'),
    # ex : /api/sec_add_event_list/
    path('sec_add_event/', views_if_sec.add_event, name='add_event'),
    # ex : /api/sec_get_guest_list/
    path('sec_get_guest_list/', views_if_sec.get_guest_list, name='get_guest_list')

]
