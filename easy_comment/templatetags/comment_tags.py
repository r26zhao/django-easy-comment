from django import template
from django.conf import settings
from django.apps import apps
from django.db.models.aggregates import Count

from ..forms import CommentForm
from ..models import Comment

register = template.Library()


@register.simple_tag
def generate_form(entry=None):
    if entry:
        form = CommentForm(initial={'entry': entry.id})
    else:
        form = CommentForm()
    return form


@register.simple_tag
def get_comment_list(entry):
    if entry:
        queryset = entry.comments.all()
    else:
        queryset = Comment.objects.filter(entry=None)
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
