# django-easy-comment
 django-easy-comment 是一个评论插件，功能包括评论，层级回复，点赞，（email && 站内）通知。在线参考地址：**http://www.aaron-zhao.com/post/6/#cmt-form**
 ![image](http://www.aaron-zhao.com/media/upload/Aaron/2017/08/02/vzlhpz.png)

 评论框编辑器使用的[**django-ckeditor**](https://github.com/django-ckeditor/django-ckeditor)

 层级回复功能用[**django-mptt**](https://github.com/django-mptt/django-mptt)实现的，mptt在后台会记录层级回复的顺序

 通知功能使用的[**django-notifications-hq**](https://github.com/django-notifications/django-notifications)

## 更新 2017.08.07
### 增加站内实时通知
开启站内通知，在```base.html```模板里引入```notifications/notice.js```


```
<script src="{% static 'notifications/notice.js' %}"></script>
```

如果想要显示未读通知的数量，写一个```<span class="live-notify-badge"><span>```，```notice.js```脚本会自动更新，每30秒一次。
## 开发环境
django 1.11, python 3.4
## 安装
1. 使用pip安装```django-ckeditor```, ```django-mptt```, ```django-notifications-hq```

```
pip install django-ckeditor
pip install django-mptt
pip install django-notifications-hq
```

2. 从github把```easy_comment``` 和 ```online_status```拉取到本地项目
3. 在settings.py里把上面安装的app加入到```INSTALLED_APPS```中

```
INSTALLED_APPS = [
    'ckeditor',
    'ckeditor_uploader',
    'mptt',
    'easy_comment',
    'notifications',
    'online_status',
]

COMMENT_ENTRY_MODEL = 'xxx' # 格式是 app_name+model_name
AUTH_USER_MODEL = 'xxx'     # 格式是 app_name+model_name
```
```COMMENT_ENTRY_MODEL```设置将评论绑定到哪个object上，比如我的评论是绑定到blog app下的Post模型中，```COMMENT_ENTRY_MODEL = "blog.post"```

```AUTH_USER_MODEL``` 规定了使用User的model，默认是```auth.user```, django自带的用户模型

添加```ckeditor```相关设置，使编辑器可以添加代码块，上传图片

```
#ckeditor setup
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
CKEDITOR_UPLOAD_PATH = 'upload/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        # 编辑器的宽高请根据你的页面自行设置
        'width':'730px',
        'height':'150px',
        'image_previewText':' ',
        'tabSpaces': 4,
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Format', 'RemoveFormat'],
            ['NumberedList', 'BulletedList'],
            ['Blockquote', 'CodeSnippet'],
            ['Image', 'Link', 'Unlink']
        ],
        'extraPlugins': ','.join(['codesnippet','uploadimage','prism','widget','lineutils',]),
    }
}
CKEDITOR_ALLOW_NONIMAGE_FILES = False
# 限制用户查看上传图片的权限， 只能看自己传的图片
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_RESTRICT_BY_DATE = True
CKEDITOR_BROWSE_SHOW_DIRS = True
```
更多ckeditor的设置，可以参考下这里：[**django博客开发：添加富文本编辑器ckeditor**](http://www.aaron-zhao.com/post/1/)

4. 在项目的urls.py里加入easy_comment, ckeditor_upload 和 notification的url

```
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
import notifications.urls

urlpatterns = [
    url(r'', include('ckeditor_uploader.urls')),
    url(r'', include('easy_comment.urls')),
    url(r'^notifications/', include(notifications.urls, namespace='notifications')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
5. 不要忘记数据库迁移

```
python manage.py makemigrations
python manage.py migrate
```

## 使用
### example
在easy_comment的templates中我写了两个模板文件```comment_form.html``` 和 ```comment_list.html```，分别在用来显示评论框和评论列表。在你的```blog_detail.html```模板中，把它们放在显示评论的位置即可。

```
{% include 'easy_comment/comment_form.html' with post=传递给模板的变量名 %}
{% include 'easy_comment/comment_list.html' with post=传递给模板的变量名 %}
```
这里的post是detai view通过context字典传递给模板的变量，如果你使用了不一样的变量名，比如```context = {"article" : article}```, 则需要```post=article```

评论模板使用了bootstrap，评论、点赞在前端用ajax处理post请求，需要引入静态文件

```
<link rel="stylesheet" href="//cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css">
<script src="http://cdn.bootcss.com/jquery/2.1.4/jquery.min.js"></script>
<!-- 评论框、评论列表和通知列表的样式 -->
<link rel="stylesheet" href="{% static 'easy_comment/css/comment.css' %}">

<!-- 代码块的高亮 -->
<link rel="stylesheet" href="{% static 'easy_comment/css/prism.css' %}">
<script src="{% static 'ckeditor/ckeditor/plugins/prism/lib/prism/prism_patched.min.js' %}"></script>
```


## 自定义模板
如果你要自定义评论模板的话，下面的模板标签可以方便使用
### 模板标签
在使用模板标签之前，先加载```{% load comment_tags %}```

```generate_form_for``` 在模板中生成评论框，用法如下

```
<!-- post是你通过view传递给模板的 -->
{% generate_form_for post as form %}

<form class="comment-form" id="cmt-form" method="post" action="{% url'easy_comment:submit_comment' post.id %}">
   {% csrf_token %}
   {% for field in form %}
   {{ field }}
   {{ field.errors }}
   {% endfor %}
   <button class="btn btn-primary pull-right" type="submit">提交评论</button>
</form>

<!-- 在非admin后台的地方使用django-ckeditor，需要引入这两个js -->
<script type="text/javascript" src="{% static "ckeditor/ckeditor-init.js" %}"></script>
<script type="text/javascript" src="{% static "ckeditor/ckeditor/ckeditor.js" %}"></script>
```
```get_comment_list_of``` 获取一篇文章的评论列表, **example:**

```
{% get_comment_list_of post as comment_list %}
```
```get_comments_user_count``` 获取一篇文章的评论人数， **example:**

```
{% get_comments_user_count post as user_count %}
```
```get_like_count``` 和 ```get_dislike_count``` 分别用了获取某条评论的点赞数量和踩的数量， **example**

```
{% get_like_count comment as like_num %}
```
```get_comment_rank``` 获得评论数排名前5（默认）的文章列表, **example**

```
{% get_comment_rank as post_list %}
```
## 评论通知
每当用户发表一条评论、回复或者点赞、踩，都会生成notification实例，管理员（admin）可以收到所有通知，普通用户可以收到与自己相关的评论、回复和点赞（踩 看不到）。

在settings.py里添加ADMINS，需要提供管理员的用户名和邮箱。
```
ADMINS = (('Aaron', 'rudy710@qq.com'),)  # 网站管理员
```
开启站内通知，在base.html模板里引入notifications/notice.js

```
<script src="{% static 'notifications/notice.js' %}"></script>
```
如果想要显示未读通知的数量，写一个```<span class="live-notify-badge"><span>```，notice.js脚本会自动更新，每30秒一次。
![image](http://www.aaron-zhao.com//media/upload/Aaron/2017/08/03/ofpkpf.png)

```/notifications/``` 当前登录用户的所有通知

```/notifications/unread``` 当前用户的未读通知


### 模板标签
使用之前先加载  ```{% load notifications_tags %}```

```{% notifications_unread %}``` 获取未读通知数

## 邮件通知
默认情况下是不发邮件通知的。开启邮件通知功能后，只有当用户不在线的情况下，才会发邮件。

```
SEND_NOTIFICATION_EMAIL = True   # 开启邮件通知

# SMTP设置
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT =
EMAIL_USE_SSL =
```
添加```'online_status.middleware.OnlineStatusMiddleware'``` 到 ```MIDDLEWARE```

```
MIDDLEWARE = [
    ···
    ···
    ···
    'online_status.middleware.OnlineStatusMiddleware',
]
```
判断用户是否在线，是通过判断用户在一定时间范围内是否有发送新的request，如果超出时间范围，视为不在线。这是时间是通过 ```USER_ONLINE_TIMEOUT``` 来设置，默认是600秒，也就是10分钟。

```
USER_ONLINE_TIMEOUT = 600
```
## 关于django-ckeditor
默认情况下django-ckeditor设置的只允许管理员发送图片，要让普通用户也可以发图片的话，需要ckeditor_uploader/urls.py里进行修改,它的```upload``` 和 ```browse```方法用了```staff_member_required```装饰器，把它换成```login_required```装饰器即可。

```
if django.VERSION >= (1, 8):
    urlpatterns = [
        url(r'^upload/', login_required(views.upload), name='ckeditor_upload'),
        url(r'^browse/', never_cache(login_required(views.browse)), name='ckeditor_browse'),
    ]
```

## 联系
Email：rudy710@qq.com

QQ：370297300

Blog：www.aaron-zhao.com

有问题的话，欢迎大家随时交流