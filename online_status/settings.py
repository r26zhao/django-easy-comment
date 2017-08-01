from django.conf import settings

USER_ONLINE_TIMEOUT = getattr(settings, 'USER_ONLINE_TIMEOUT', 600)
USER_LAST_LOGIN_EXPIRE = getattr(settings, 'USER_LAST_LOGIN_EXPIRE', 60 * 60 * 24 * 7)
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')