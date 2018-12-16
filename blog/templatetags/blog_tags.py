from ..models import Post, Category, Tag
from django import template
from django.db.models.aggregates import Count

register = template.Library()

# 最新文章 模板标签
@register.simple_tag
def get_recent_post(num=5):
    return Post.objects.all().order_by('-created_time')[:num]

# 归档模板标签
@register.simple_tag
def get_archives():
    return Post.objects.dates('created_time', 'month', order='DESC')
    # return Post.objects.annotate(num_posts=Count('post')).dates('created_time', 'month', order='DESC')


# 分类模板标签
@register.simple_tag
def get_category():
    return Category.objects.all()


@register.simple_tag
def get_tag():
    return Tag.objects.annotate(num_posts=Count('post'))
    # 计数的时候用Tag.num_posts