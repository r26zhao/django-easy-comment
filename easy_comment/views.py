from .forms import CommentForm
from .models import Comment, Like
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from . import handlers

# Create your views here.

@require_POST
def submit_comment(request, id):
    form = CommentForm(data=request.POST)
    # print(request.POST)
    if form.is_valid():
        # print('success')
        new_comment = form.save(commit=False)
        new_comment.user = request.user
        new_comment.user_name = request.user.username
        new_comment.save()
        location = "#c" + str(new_comment.id)
        return JsonResponse({'msg':'success!', 'new_comment':location})
    return JsonResponse({'msg':'评论出错!'})

@require_POST
def like(request):
    comment_id = request.POST.get('id')
    action = request.POST.get('action')
    if comment_id and action:
        try:
            comment = Comment.objects.get(id=comment_id)
            obj, created = Like.objects.get_or_create(user = request.user, comment = comment)
            if action == 'like':
                if not created:
                    obj.status = True
                    obj.save()
            if action == 'cancel-like' or action == 'cancel-dislike':
                obj.delete()
            if action == 'dislike':
                obj.status = False
                obj.save()
            return JsonResponse({'msg':'OK'})
        except Comment.DoesNotExist:
            return JsonResponse({"msg":"KO"})
    return JsonResponse({"msg":"KO"})