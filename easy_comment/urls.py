from django.conf.urls import url

from . import views


app_name = 'easy_comment'
urlpatterns = [
    url(r'^submit-comment/$', views.submit_comment, name='submit_comment'),
    url(r'^entry/(?P<pk>\d+)/comment-list/', views.comment_list, name='comment_list'),
    url(r'^comment-list/$', views.comment_list, name='comment_list_no_object')
]
