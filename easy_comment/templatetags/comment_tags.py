from django import template
from ..forms import CommentForm

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