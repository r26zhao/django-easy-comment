from django.db import models
from . import settings
from django.core.cache import cache
import datetime
from django.utils import timezone
# Create your models here.

class OnlineStatus(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_login = models.DateTimeField(default=timezone.now)
    class Meta:
        verbose_name = 'Online Status'
        verbose_name_plural = 'Online Status'
        ordering = ['-last_login']

    def __str__(self):
        return '%s last login at UTC %s' % (self.user.username, self.last_login.strftime('%Y/%m/%d %H:%M'))

    def get_last_active(self):
        cache_key = '%s_last_login' % self.user.username
        # 如果缓存过期，从数据库获取last_login，并存到缓存
        if not cache.get(cache_key):
            print("####### index view -- cache not found")
            cache.set(cache_key, self.last_login, settings.USER_LAST_LOGIN_EXPIRE)
        return cache.get(cache_key)

    def is_online(self):
        now = timezone.now()
        if self.get_last_active() < now - datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
            return False
        return True