from django import template
from django.conf import settings
from django.apps import apps
from django.db.models.aggregates import Count
from django.contrib.contenttypes.models import ContentType

from ..forms import CommentForm
from ..models import Comment

register = template.Library()


@register.simple_tag
def generate_form(entry=None):
    if entry:
        content_type = ContentType.objects.get_for_model(entry)
        form = CommentForm(initial={'content_type': content_type.id,
                                    'object_id': entry.id})
    else:
        form = CommentForm()
    return form


@register.simple_tag
def get_comment_list(entry):
    if entry:
        content_type = ContentType.objects.get_for_model(entry)
        queryset = Comment.objects.filter(content_type=content_type, object_id=entry.id)
    else:
        queryset = Comment.objects.filter(content_type=None)
    return queryset


@register.simple_tag
def get_comments_user_count(entry):
    queryset = get_comment_list(entry=entry)
    user_list = []
    for comment in queryset:
        if comment.user not in user_list:
            user_list.append(comment.user)
    user_count = len(user_list)
    return user_count


@register.simple_tag
def get_content_type_id(entry):
    if entry:
        content_type = ContentType.objects.get_for_model(entry)
        return content_type.id
    else:
        return ''