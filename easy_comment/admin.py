from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Comment, Like
# Register your models here.

admin.site.register(Comment, MPTTModelAdmin)
admin.site.register(Like)