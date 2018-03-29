与之前的版本相比主要的差别是现在评论使用ajax异步加载、支持评论分页（下拉无限加载），无须再绑定模型，可以评论任何对象（也可以是空的），目前采用的一级评论，按时间倒序，但是评论模型依旧继承了MPTTModel来记录层级顺序，未来会加入二级评论和多层级评论的模板供大家选择。

## 项目地址

[https://github.com/r26zhao/django-easy-comment](https://github.com/r26zhao/django-easy-comment)  如果觉得对你有所帮助的话，请给个star (◕ᴗ◕✿)
开发环境：py3.6、Django1.11

目前没有在py2.7测试过，但根据使用py2.7的小伙伴反应，会报出编码错误，由easy_comment/handlers.py 文件里的中文引起的，把里面的中文处理一下即可解决。
## 安装

1.从github把`easy_comment`、`online_status`和`requirements`拉取到本地项目

2.安装依赖包

 `pip install -r requirements/requirements.txt`

3.在settings.py里把上面安装的app加入到`INSTALLED_APPS`中
```
INSTALLED_APPS = [
    'ckeditor',
    'ckeditor_uploader',
    'mptt',
    'easy_comment',
    'notifications',
    'online_status',
]
```
添加ckeditor相关设置，使编辑器可以添加代码块，上传图片
```
#ckeditor setup
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
CKEDITOR_UPLOAD_PATH = 'upload/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'width':'auto',
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
更多ckeditor的设置，可以参考下这里：[django博客开发：添加富文本编辑器ckeditor](http://www.aaron-zhao.com/post/1/)

4.`settings.py`里的其他设置
```
AUTH_USER_MODEL = 'xxx'     # 格式是 app_name+model_name
SEND_NOTIFICATION_EMAIL = False
COMMENT_PAGINATE_BY = 10
```
**AUTH_USER_MODEL** 规定了使用User的model，默认是auth.User, django自带的用户模型

**SEND_NOTIFICATION_EMAIL** 设置是否接收评论通知邮件，默认False 不接收

**COMMENT_PAGINATE_BY** 设置评论分页，比如10，就是每10条评论一页，如果设置为None，则不分页，默认10

5.在项目的urls.py里加入`easy_comment`, `ckeditor_upload` 和 `notification`的url
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

6.迁移数据库
```
python manage.py makemigrations
python manage.py migrate
```
## 使用模板

在detail.html（显示文章）模板里，显示评论的地方引入评论模板
```
{% include 'easy_comment/comment.html' with entry=传递给模板的变量名 %}
```
这里的entry是detai视图函数通过context字典传递给模板的变量，如果你使用了不一样的变量名，比如`context = {"article" : article}`, 则写`entry=article`
### 评论对象为空

如果你评论的对象是空的，需要在comment.html的第129、147行把 `{% url 'easy_comment:comment_list' entry.id %}` 改为 `{% url 'easy_comment:comment_list_no_object' %}`
## 引入静态文件
```
<link href="https://cdn.bootcss.com/Buttons/2.0.0/css/buttons.min.css" rel="stylesheet">
<link href="https://cdn.bootcss.com/font-awesome/4.3.0/css/font-awesome.min.css" rel="stylesheet">
<!-- 评论框、评论列表的样式 -->
<link rel="stylesheet" href="{% static 'easy_comment/css/comment.css' %}">

<!-- 代码块的高亮 -->
<link rel="stylesheet" href="{% static 'easy_comment/css/prism.css' %}">
<!-- jquery要放在其他script上面 -->
<script src="https://cdn.bootcss.com/jquery/1.8.3/jquery.min.js"></script>
<script src="{% static 'ckeditor/ckeditor/plugins/prism/lib/prism/prism_patched.min.js' %}"></script>
```
## 通知功能

每当用户发表一条评论、回复，都会生成一个notification实例，管理员（admin）可以收到所有通知，普通用户仅可以收到与自己相关的回复通知，自己对自己的回复是不会产生通知的。
## 添加管理员

在`settings.py`里添加ADMINS，需要提供管理员的用户名和邮箱。
```
ADMINS = (('Aaron', 'rudy710@qq.com'),)  # 网站管理员
```
## 开启站内通知

在base.html模板里引入`notifications/notice.js`
```
<script src="{% static 'notifications/notice.js' %}"></script>
```
如果想要显示未读通知的数量，写一个`<span class="live-notify-badge"></span>`，notice.js脚本会自动更新并向这个span里添加数据，每30秒一次。



`/notifications/ `当前登录用户的所有通知

`/notifications/unread` 当前用户的未读通知
## 开启邮件通知

默认情况下是不发邮件通知的。开启邮件通知功能后，只有当用户不在线的情况下，才会发邮件。
```
SEND_NOTIFICATION_EMAIL = True   # 开启邮件通知

# SMTP设置
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT =
EMAIL_USE_SSL =

添加'online_status.middleware.OnlineStatusMiddleware' 到 MIDDLEWARE

MIDDLEWARE = [
    ···
    ···
    ···
    'online_status.middleware.OnlineStatusMiddleware',
]

USER_ONLINE_TIMEOUT = 600
```

判断用户是否在线，是通过判断用户在一定时间范围内是否有发送新的request，如果超出时间范围，视为不在线。这是时间是通过 `USER_ONLINE_TIMEOUT` 来设置，默认是600秒，也就是10分钟。
## 关于django-ckeditor

默认情况下`django-ckeditor`设置的只允许管理员发送图片，要让普通用户也可以发图片的话，需要`ckeditor_uploader/urls.py`里进行修改,它的`upload` 和 `browse`方法用了`staff_member_required`装饰器，把它换成`login_required`装饰器即可。
```
if django.VERSION >= (1, 8):
    urlpatterns = [
        url(r'^upload/', login_required(views.upload), name='ckeditor_upload'),
        url(r'^browse/', never_cache(login_required(views.browse)), name='ckeditor_browse'),
    ]
```
## 总结

其实实现一个评论功能并不难，更多的时间是花在如何在前端显示加载评论。本文采用的是后端view返回json，然后前端调用api，ajax异步加载，某种程度上也算是前后分离了。说到前后分离，就要扯到restful api了，后面会介绍下[django-rest-framework](https://github.com/encode/django-rest-framework/tree/master) 的使用（给自己挖个坑）。



ok，扯到这里吧，大家有任何问题，随时交流，评论区留言或者qq（370297300）联系。
