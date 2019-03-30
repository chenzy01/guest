from django.contrib import admin
from sign.models import Event, Guest

# Register your models here.让界面显示更多的字段
class EventAdmin(admin.ModelAdmin):
    #定义要在列表中显示哪些字段（界面上）
    list_display = ['id', 'name', 'status', 'address', 'start_time']
    search_fields = ['name'] #创建字段搜索栏
    list_filter = ['status'] #创建字段过滤器

class GuestAdmin(admin.ModelAdmin):
    list_display = ['realname', 'phone', 'email', 'sign', 'create_time', 'event']
    search_fields = ['realname', 'phone']
    list_filter = ['sign']

admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)