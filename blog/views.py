from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify

from blog.models import Post, Category, Tag
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView, View, DetailView
# Create your views here.

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    # ListView已经写好了分页的逻辑
    # 我们只需指定paginate_by属性，开启分页功能，其值代表一页包含多少篇文章
    paginate_by = 10
    # 然后去模板页设置分页导航

    # 以下是升级版的分页效果
    def get_context_data(self, *, object_list=None, **kwargs):
        # 首先获得父类生成的传递给模板的字典。
        context = super().get_context_data(**kwargs)

        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated =context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        context.update(pagination_data)

        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        left = []
        right = []
        left_has_more = False
        right_has_more = False

        first = False
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页的页码列表
        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True

        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data




# 用来查询，排序等一系列操作
    def get_queryset(self):
        return super().get_queryset().all().order_by('-created_time')

# /blog/index
def index(request):
    post_list = Post.objects.all().order_by('-modified_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_read_nums()

        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)

        md = markdown.Markdown(extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
            TocExtension(slugify=slugify),
                                      ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list,
        })
        return context


# /blog/detail
def detail(request, id):
    post = get_object_or_404(Post, id=id)
    post.increase_read_nums()
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',

                                  ])

    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list,
    }
    return render(request, 'blog/detail.html', context=context)


class ArchivesView1(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        x = get_object_or_404(Post, id=self.kwargs.get('created_time'))
        return super().get_queryset().filter(created_time__year=x.created_time.year,
                                    created_time__month=x.created_time.month).order_by('-created_time')

class ArchivesView(View):
    def get(self, request, year, month):
        '''点击归档之后页面显示的内容'''
        post_list = Post.objects.filter(created_time__year=year,
                                        created_time__month=month).order_by('-created_time')
        return render(request, 'blog/index.html', context={'post_list': post_list})


# /blog/archives/year/month
# 无法获得确切的年月，因为用了MySQL DB？
# 在settings中将USR_TZ改成True就好了
def archives(request, year, month):
    '''点击归档之后页面显示的内容'''
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})

class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, id=self.kwargs.get('id'))
        return super(CategoryView, self).get_queryset().filter(category=cate).order_by('-created_time')

# /blog/category/id
def category(request, id):
    '''点击分类的类名后显示的页面'''
    # 获得一个模型类Category的实例，id由页面传入
    cate = get_object_or_404(Category, id=id)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, id=self.kwargs.get('id'))
        return super().get_queryset().filter(tag=tag).order_by('-created_time')

# search/
def search(request):
    q = request.GET['q']
    error_msg = ''

    if not q:
        error_msg = '查询不到相关结果，请换一个关键词！'
        return render(request, 'blog/index.html', {'error_msg':error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'error_msg':error_msg,
   'post_list':post_list})


def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

@csrf_exempt
def handle_contract(request):
    pass