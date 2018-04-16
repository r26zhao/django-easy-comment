from mptt.models import TreeForeignKey, MPTTModel
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.


class Comment(MPTTModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name='父级评论')
    content = RichTextUploadingField(verbose_name='评论', config_name='default')
    created = models.DateTimeField(auto_now_add=True, verbose_name='提交时间')

    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        if self.parent is not None:
            return '{} 回复 {}'.format(self.user.username, self.parent.user.username)
        if self.content_object:
            return '{} 评论 {}_{}'.format(self.user.username, self.content_type.model, self.object_id)
        else:
            return '{} 发表了评论'.format(self.user.username)

    def to_html(self):
        """
        把每一条comment的内容渲染成html，并保存在缓存里，不需要每次都渲染了
        :return html
        """
        key = "comment_{}_html".format(self.id)
        html = cache.get(key)
        if not html:
            html = render_to_string('easy_comment/comment_entry.html', context={'comment': self})
            cache.set(key, html, timeout=600)
        return html
