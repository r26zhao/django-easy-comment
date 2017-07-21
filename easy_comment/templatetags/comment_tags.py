from django import template
from ..forms import CommentForm
from ..models import Like

register = template.Library()

@register.simple_tag
def generate_form_for(post):
    form = CommentForm(initial={'post':post.id})
    return form

@register.simple_tag
def get_comment_list_of(post):
    return post.comment_set.all()

@register.simple_tag
def get_comments_user_count(post):
    user_list = []
    for comment in post.comment_set.all():
        if not comment.user in user_list:
            user_list.append(comment.user)
    return len(user_list)

@register.simple_tag
def get_like_action(user, comment):
    if user.is_anonymous:
        return 0
    try:
        obj = Like.objects.get(user = user, comment = comment)
        return 1 if obj.status else -1
    except Like.DoesNotExist:
        return 0

@register.simple_tag
def get_like_count(comment):
    return comment.like_set.filter(status = True).count()

@register.simple_tag
def get_dislike_count(comment):
    return -comment.like_set.filter(status = False).count()