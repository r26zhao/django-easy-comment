from django.db import models
from django.conf import settings
from mptt.models import TreeForeignKey, MPTTModel
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Comment(MPTTModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,)
    user_name = models.CharField(max_length=50, blank=True, null=True)
    post = models.ForeignKey(settings.COMMENT_ENTRY_MODEL, verbose_name='文章')
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name='父级评论')
    content = RichTextUploadingField(verbose_name='评论', config_name='default')
    submit_date = models.DateTimeField(auto_now_add=True, verbose_name='提交时间')

    class MPTTMeta:
        order_insertion_by = ['submit_date']

    def __str__(self):
        if self.parent is not None:
            return '%s 回复 %s' % (self.user_name, self.parent.user_name)
        return '%s 评论文章 post_%s' % (self.user_name, str(self.post.id))

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    comment = models.ForeignKey(Comment)
    created_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = '点赞'
        verbose_name_plural = verbose_name
    def __str__(self):
        if self.status:
            return '%s 赞了 %s的评论' % (self.user.username, self.comment.user_name)
        return '%s 踩了 %s的评论' % (self.user.username, self.comment.user_name)