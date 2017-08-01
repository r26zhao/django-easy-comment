import datetime
from django.utils import timezone
from django.core.cache import cache
from . import settings
from .models import OnlineStatus
from django.utils.deprecation import MiddlewareMixin

class OnlineStatusMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated():
            cache_key = '%s_last_login' % request.user.username
            now =timezone.now()
            # 用户是第一次登录、或者是缓存过去、或者是服务器重启导致缓存消失
            if not cache.get(cache_key):
                # print('#### cache not found #####')
                obj, created = OnlineStatus.objects.get_or_create(user=request.user)
                if not created:
                    # print("#### login before #####")
                    obj.last_login = now
                    obj.save()
                cache.set(cache_key, now, settings.USER_LAST_LOGIN_EXPIRE)
            else:
                # print("##### cache found ######")
                limit = now - datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)
                # 距离上一次发送request请求的时间 超过了TIMEOUT，更新上一次login的时间
                if cache.get(cache_key) < limit:
                    # print("#### renew login #####")
                    obj = OnlineStatus.objects.get(user=request.user)
                    obj.last_login = now
                    obj.save()
                cache.set(cache_key, now, settings.USER_LAST_LOGIN_EXPIRE)
        return None