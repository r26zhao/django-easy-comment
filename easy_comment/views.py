from django.shortcuts import render, redirect
from .forms import CommentForm
from .models import Comment
from django.http import JsonResponse, HttpResponse
# Create your views here.

def submit_comment(request, id):
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        print(request.POST)
        if form.is_valid():
            print('success')
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.user_name = request.user.username
            new_comment.save()
            location = "#c" + str(new_comment.id)
            return JsonResponse({'msg':'success!', 'new_comment':location})
        return JsonResponse({'msg':'评论出错!'})
    return redirect(request.path.replace('submit-comment/', ''))