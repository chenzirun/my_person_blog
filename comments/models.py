from django.db import models
from blog.models import Post
# Create your models here.



class Comment(models.Model):
    '''评论区块的数据库模型'''
    # 用户名
    name = models.CharField(max_length=100, verbose_name='用户名')
    # 电子邮件
    email = models.EmailField(max_length=200, verbose_name='电子邮件')

    # 评论内容
    text = models.TextField(verbose_name='评论内容')
    # 时间
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='时间')
    # 外链
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:200]