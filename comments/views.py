from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from .forms import CommentForm
from .models import Comment

# Create your views here.

# /comments/post/id
def post_comment(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        # 利用传过来的数据创建实例以渲染表单
        form = CommentForm(request.POST)

        # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
        if form.is_valid():
            comment = form.save(commit= False)

            comment.post = post

            comment.save()

            #return redirect(post)
            return  redirect(f'/blog/detail/{id}')
        else:
            comment_list = post.comment_set.all()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list,
            }
            render(request, 'blog/detail.html', context=context)

    return redirect(f'/blog/detail/{id}')