from django.contrib import admin
from .models import Category,Tag,Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    '''定制网站后台管理页面'''
    list_display = ['title', 'category', 'created_time', 'modified_time', 'read_nums', 'author', ]

    

admin.site.register(Category)
admin.site.register(Tag)
# 不要忘记PostAdmin也要注册
admin.site.register(Post, PostAdmin)
