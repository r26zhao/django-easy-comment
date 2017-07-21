from django.conf.urls import url
from . import views

app_name = 'easy_comment'
urlpatterns = [
    url(r'^post/(?P<id>[0-9]+)/submit-comment/$', views.submit_comment, name='submit_comment'),
    url(r'^comment/like/$', views.like, name='like'),
]