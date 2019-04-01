## 第一个Django demo
### 平台：Pycharm Django
***

使用 Pycharm 进行开发，需要提前在 Pycharm 中（File > Settings > Project: Python > Project Interpreter）下载 Django ，安装过程会自动把 Django 路径加载到系统的环境变量中。

进入 cmd 查询 Django 是否安装成功。出现以下一系列命令，说明已安装成功。
![image](https://github.com/chenzy01/guest/blob/master/image/%E6%9F%A5%E7%9C%8BDjango%E6%98%AF%E5%90%A6%E5%AE%89%E8%A3%85%E6%88%90%E5%8A%9F.png)


创建第一个项目 guest ，可在 Pycharm 的 Terminal 中使用命令行创建

G:\Python>django-admin startproject guest

创建完成，Django 自动生成以下目录结构

guest/guest/__init__.py : 空文件夹，表示 guest 目录是 python 的标准包

guest/guest/settings.py : 项目的配置文件，包含Django 模块应用配置、数据库配置、模板配置等

guest/guest/urls.py : 关于项目的 URL 声明，定义 URLconf

guest/guest/wsgi.py : 提供服务的入口，暂未知 wsgi 有何用

guest/manage.py : 一个命令行工具，通过 命令  python manage.py 可以查看 manage 所提供的命令

 

#### 创建第一个应用

G:\Python\guest>python mangage.py startapp sign

在 Terminal 中使用以上命令创建 sign 应用（模块）后，会自动生成一些文件（templates 目录不是自动生成），如下面目录结构：
![image](https://github.com/chenzy01/guest/blob/master/image/%E5%88%9B%E5%BB%BA%E7%AC%AC%E4%B8%80%E4%B8%AA%E5%BA%94%E7%94%A8.png)  

创建完 sign 模块后，需要将 sign 添加到 settings.py 中的 INSTALLED_APPS 中，告诉 Django 有这么一个应用

'''python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sign',
]
'''


#### 目录文件说明：

migrations/ : 用于记录models 中数据的变更

admin.py : 映射 models 中的数据到 Django 自带的后台

apps.py : 用于应用程序配置

models.py : 创建数据表模型，与数据库相关操作对应

views.py : 视图文件，控制向前端输送内容

 
#### 启动项目，使用 runserver 命令

G:\Python\guest>python manage.py runserver

Django 默认在127.0.0.1:8000 进行监听，在浏览器输入 http://127.0.0.1:8000 , 若可见 It worked! 提示，说明 Django 已经可以工作。

PS: Django 在 settings.py 中默认开启 DEBUG = True，若改为 False ，则无法正常打开网页。 127.0.0.1 指向本机（本电脑）

#### 使用模板

创建模板使用 templates 目录，Django 会默认去查找该目录下面的 HTML 文件，在上面已创建的 sign 应用下面，创建了一个

templates/index.html 文件

#### 简述 Django 工作流 
（以默认访问的地址为例）：

向浏览器发送一个请求，如 http://127.0.0.1:8000/index/ ，Django 默认在127.0.0.1地址，端口8000 上进行监听，根据 URL 的路径 /index/，

到 urls.py 文件中对 /index/ 路径进行匹配（前提：在 urls.py 中对该路径已进行配置），匹配到该路径，则调用相应的视图函数，匹配不到，则提示网页找不到（404）。

url 路径匹配模式如下：
```Python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index), #添加index/ 路径配置
]
```

上面/index/ 路径已经提前配置好，下一步根据路径，去调用相应的视图函数 views.index （请求指向 sign 应用下的 views.py 文件中的 index 函数）。该函数定义如下：

```Python
def index(request):
    return render(request, "index.html")
```

该函数使用 render 模板，返回一个已经写好的 HTML 页面。该模板放在 templates 目录下，使用render() 函数进行调用，浏览器最终呈现 index.html 页面的内容（返回响应）。



#### 各模块要点

#### Django MTV 开发模式

M(Models): 代表模型，进行数据存取。处理与数据相关的事物，既如何存取，如何验证有效。

T(Template): 代表模板，表现层。处理如何展示相关页面或其它类型文档。

V(View): 代表视图，业务逻辑层。处理如何存取模型及调用恰当的模板展现数据，可看做是模型与模板之间的桥梁。

#### URLconf模块  urls.py

1、URLconf 模块包含了 URL 模式（简单的正则表达式）到视图函数（views.py）的简单映射。URLconf的值通过 ROOT_URLCONF 进行设置，
在 /settings.py 中  
'''python
ROOT_URLCONF = 'guest.urls'
'''
Django 会加载 urls.py 文件，并在 urlpatterns 中依次匹配每个 URL 模式，匹配到就指向对应的视图函数处理。


#### views.py 

1、 index() 视图函数，接受 Web 请求并且返回 Web 响应

2、 login_action(request) 处理登录请求,客户端发送的请求信息都包含在 request 中。request.POST 通过 .get() 方法获取“username”和“password”所获取的用户名和密码

3、 HttpResponseRedirect() 对路径进行重定向，将登录成功后的请求指向了 /event_manage/ 目录

4、 render()方法：render(request, template_name, context=None, content_type=None, status=None, using=None)  
作用：把 context（一个给定的上下文字典）的内容, 加载进 templates（一个给定的模板）中定义的文件, 并通过浏览器渲染呈现.
参数讲解:
request: 是一个固定参数.

template_name: templates 目录下定义的文件, 要注意路径名. 比如'templates\polls\index.html', 参数就要写‘polls\index.html’

context: 要传入文件中用于渲染呈现的数据, 默认是字典格式

content_type: 生成的文档要使用的MIME 类型。默认为DEFAULT_CONTENT_TYPE 设置的值。

status: http的响应代码,默认是200.

using: 用于加载模板使用的模板引擎的名称。

5、auth.authenticate() 方法，用于登录认证。它接受两个参数，用户名 username 和 密码 password ，并在用户名和密码正确的情况下返回一个 User 对象。 否则 authenticate() 返回None。

6、auth.login() 方法，用于用户登录。该函数接受一个 HttpRequest 对象和一个 User 对象作为参数并使用Django的会话（session）框架把用户的ID保存在该会话中。

7、user.is_active 判断用户名和密码是否有效。

8、 @login_required 此装饰器显限制某个视图函数必须登录才能访问，默认跳转的 URL 中会包含“/accounts/login/”，需要在 urls.py 中添加新的路径配置。

#### templates 模板

1、使用模板动态的生成 HTML

2、简单了解两个方法：GET 和 POST  
GET: 从指定的资源请求数据，一般用于查询数据；  
POST: 向指定的资源提交要被处理的数据，一般用于更新数据，提交表单。

3、GET 方法将用户提交的数据添加到 URL 中，路径后面跟问号 “？”，用于区分路径和参数（问号后面是参数），多个参数之间用“&”隔开。

4、 index.html 中{% csrf_token %},是CSRF令牌（跨站请求伪造），通过该令牌判断POST请求是否来自同一个网站，防止伪装提交请求的功能。

5、 form 表单中的 action="/login_action" 指定了提交的路径，根据该路径去 urls.py 中匹配 URL 模式，再去 views.py 中执行相应的视图。


#### models.py  

1、模型基础知识  
· 每一个 model 都是 Python 类，都要继承 django.db.models.Model 类
· 模型的每个属性表示数据库的表字段
· Django 把这一些已经给了一个自动生成的访问数据库的 API
· 创建模型时，后台会在数据库自动生成一个 id 作为主键，这个主键可以被覆盖

2、__str__()是被 print 函数调用的，__str__()返回的内容以字符串形式输出,该方法告诉 Python 如何将对象以 str 的方式显示出来。

3、类 Meta 的作用：  

模型元数据是“任何不是字段的数据”，比如排序选项（ordering），数据库表名（db_table）或者人类可读的单复数名称（verbose_name 和verbose_name_plural）。在模型中添加class Meta是完全可选的，所有选项都不是必须的。  
更多 Django 元数据选项 ![Django Meta](https://docs.djangoproject.com/en/2.1/ref/models/options/)  

4、makemigrations 与 migrate 命令的作用  
在 models.py 中设计好模型后，需要将模型中的各个属性（或改动）映射到数据库中，首先通过 makemigrations 命令操作  
`\guest> python manage.py makemigrations sign`  
相当于在该 sign 应用中的 migrations 目录，记录了所有的关于 modes.py 的改动（比如添加字段，删除模型等），会自动生成 0001_initial.py 记录操作， 但是这个改动还没有作用到数据库文件  
`\guest> python manage.py migrate`    
将对模型的改动作用到数据库文件，比如产生 table ，修改字段的类型等  
注意：若更换数据库，数据库迁移前要保证在建模阶段，把相关字段都填写正确和规划完整，不然迁移过程会暴露许多问题。这里说的是数据库迁移，迁移执行的是同步表字段，在 MySQL 数据库中生成表，而数据是无法复制过去的，可能迁移后需要重新造数据，不然就提前导出数据，迁移完后再导入。



#### Django shell

1、进入 Django shell 模式  
`\guest> python manage.py shell`  
在 Ipython 模式下编辑  

2、获得某个 table 中的所有对象  
table.objects.all()  
```python
In [3]: Event.objects.all()
Out[3]: <QuerySet [<Event: 荣耀发布会>]>

In [4]: Guest.objects.all()
Out[4]: <QuerySet []>  
```  

2、插入数据的两种方式  
```python
In [7]: e1 = Event(id=2, name='红米发布会', limit=20, status=True, address='北京', start_time=datetime(2016,8,10,14,0,0))
   ...: e1.save()
```  
```python
Event.objects.create(id=1, name='荣耀发布会', limit=200, status=True, address='深圳会展中心', start_time=datetime(2018,9,22,14,0,0))
```

3、查询数据  
table.objects.get() 
```python
In [14]: e1 = Event.objects.get(name='红米 MAX 发布会')
In [15]: e1
Out[15]: <Event: 红米 MAX 发布会>
In [16]: e1.address
Out[16]: '北京会展中心'
```

4、过滤数据  
table.objects.filter()  相当于 SQL 语句中的 LIKE 语句   
```python
In [18]: e2 = Event.objects.filter (name__contains='发布会')
In [19]: e2
Out[19]: <QuerySet [<Event: 荣耀发布会>, <Event: 红米发布会>, <Event: 红米 MAX 发布会>]>
```

5、删除数据  
table.objects.get().delete()  
```python
In [20]: Guest.objects.get(phone='13423454334').delete()
Out[20]: (1, {'sign.Guest': 1})
```

6、更新数据  
```python
In [21]: g3 = Guest.objects.get(phone='13012345690')
In [22]: g3.realname = 'andy2'
In [23]: g3.save()
```
```python
In [24]: Guest.objects.select_for_update().filter(phone='13012345690').update(realname='andy')
Out[24]: 1
```




#### 其它

1、创建 django_session 表,存放用户 sessionid 对应的信息  
   命令：\guest> python manage.py migrate  使用 “migrate” 进行数据迁移，Django 会同时生成 auth_user 表  
   
2、Django 自带 Admin 管理后台，创建登录 Admin 后台的超级管理员账号  
   命令：\guest> python manage.py createusperuser   
   Admin 管理后台登录地址： http:127.0.0.1:8000/admin/  


   
 















