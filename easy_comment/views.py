from django.apps import apps
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.contrib.contenttypes.models import ContentType

import easy_comment.handlers
from easy_comment.forms import CommentForm
from easy_comment.templatetags.comment_tags import get_comments_user_count, get_comment_list

# Create your views here.


# 该视图函数只接受post请求, 只允许登录用户评论
@require_POST
@login_required
def submit_comment(request):
    """
    通过前端ajax post数据，生成评论，并返回评论对应的html和参与评论的用户数量、评论数量
    :param request:
    :return: JsonResponse
    """
    form = CommentForm(data=request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.user = request.user
        type_id = request.POST.get('content_type')
        object_id = request.POST.get('object_id')
        if type_id and object_id:
            content_type = ContentType.objects.get_for_id(type_id)
            content_object = content_type.get_object_for_this_type(id=object_id)
        else:
            content_object = None
        new_comment.content_object = content_object
        new_comment.save()
        cmt_list = get_comment_list(content_object).order_by('-created')
        user_count = get_comments_user_count(entry=content_object)
        comment_count = cmt_list.count()
        paginate_by = getattr(settings, 'COMMENT_PAGINATE_BY', 10)
        if paginate_by:
            cmt_list = cmt_list[: paginate_by]
        comment_list_html = ''
        for comment in cmt_list:
            comment_list_html += comment.to_html()
        return JsonResponse({'msg': 'success!',
                             'html': comment_list_html,
                             'user_count': user_count,
                             'comment_count': comment_count})
    # 如果content字段出问题了，把error记录在msg里，在前端alert
    if form.errors.as_data()['content']:
        msg = form.errors.as_data()['content'][0].message
    else:
        msg = '评论出错啦！'
    return JsonResponse({"msg": msg})


def comment_list(request, pk=None):
    """
    获取评论list，如果settings.py里设置了COMMENT_PAGINATE_BY(默认10)，则对评论分页
    设置 COMMENT_PAGINATE_BY = None则不分页
    把每一条评论的html加在一起，生成所有评论的html
    jsonresponse 里返回html，评论数量、评论人数
    :param request:
    :param pk: 被评论模型（example：文章）的pk
    :return: JsonResponse
    """
    try:
        type_id = request.GET.get('content_type')
        content_type = ContentType.objects.get_for_id(type_id)
        entry = content_type.get_object_for_this_type(id=pk)
    except Exception as e:
        entry = None
    paginate_by = getattr(settings, 'COMMENT_PAGINATE_BY', 10)
    cmt_list = get_comment_list(entry=entry).order_by('-created')
    comment_count = cmt_list.count()
    user_count = get_comments_user_count(entry=entry)
    if paginate_by:
        paginator = Paginator(cmt_list, paginate_by)
        page = request.GET.get('page', 1)
        try:
            cmt_list = paginator.page(page)
        except PageNotAnInteger:
            cmt_list = paginator.page(1)
        except EmptyPage:
            cmt_list = []
    comment_list_html = ''
    for comment in cmt_list:
        comment_list_html += comment.to_html()
    return JsonResponse({'html': comment_list_html,
                         'user_count': user_count,
                         'comment_count': comment_count})
