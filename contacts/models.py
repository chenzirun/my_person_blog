from django.db import models

# Create your models here.
class Contacts(models.Model):
    name = models.CharField(max_length=100, verbose_name='名字')
    email = models.EmailField(max_length=100, verbose_name='邮箱')
    subject = models.CharField(max_length=100, verbose_name='主题')
    message = models.TextField(verbose_name='信息')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')

    def __str__(self):
        return self.name