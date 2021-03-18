from django.contrib import admin
from django.utils import timezone

from .models import Post, Category, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'modified_time', 'create_time', 'author']
    fields = ['title', 'body', 'excerpt', 'category', 'tags']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        # obj.modified_time = timezone.now()
        super().save_model(request, obj, form, change)


# Register your models here.
# 把新增的Postadmin 也注册进来
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
