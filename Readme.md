## 第一个Django demo
### 平台：Pycharm Django

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

在 Terminal 中使用以上命令创建 sign 应用后，会自动生成一些文件（templates 目录不是自动生成），如下面目录结构：
![image](https://github.com/chenzy01/guest/blob/master/image/%E5%88%9B%E5%BB%BA%E7%AC%AC%E4%B8%80%E4%B8%AA%E5%BA%94%E7%94%A8.png)


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

简述 Django 工作流（以默认访问的地址为例）：

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
