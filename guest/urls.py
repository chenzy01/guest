"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
# 导入 sign 应用 views 文件
from sign import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),  # 添加index/ 路径配置
    path('login_action/', views.login_action),  # 指定表单提交的路径
    path('event_manage/', views.event_manage),  # 发布会管理页面
    path('accounts/login/', views.index),  # 登录
    path('search_name/', views.search_name),  # 发布会名称搜索
    path('search_phone/', views.search_phone),  # 嘉宾手机号搜索
    path('guest_manage/', views.guest_manage),  # 嘉宾
    re_path('sign_index/(?P<eid>[0-9]+)/', views.sign_index),  # 签到
    re_path('sign_index_action/(?P<eid>[0-9]+)/', views.sign_index_action),
    path('logout/', views.logout),  # 退出
    path('api/', include('sign.urls', namespace="sign")),  # 接口根路径
]
