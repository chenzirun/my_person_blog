from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Post(models.Model):
    '''博客类'''
    title = models.CharField(max_length=100, verbose_name='文章标题')
    body = models.TextField(verbose_name='文章内容')
    created_time = models.DateTimeField(auto_now=True,verbose_name='创建时间')
    modified_time = models.DateTimeField(verbose_name='更新时间')
    digest = models.CharField(max_length=200, verbose_name='摘要')

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='文章分类')
    tag = models.ManyToManyField(Tag, blank=True, verbose_name='文章标签')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='文章作者')
    read_nums = models.IntegerField(default=0,verbose_name='阅读量')

    def increase_read_nums(self):
        self.read_nums += 1
        self.save(update_fields=['read_nums'])
    def __str__(self):
        return self.title


