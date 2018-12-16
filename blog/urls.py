
from django.urls import path, include
from . import views

app_name = 'blog'
urlpatterns = [
    path('index', views.IndexView.as_view(), name='index' ),
    path('detail/<int:pk>', views.PostDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>', views.ArchivesView.as_view(), name='archives'),
    path('category/<int:id>', views.CategoryView.as_view(), name='category'),
    path('tag/<int:id>', views.TagView.as_view(), name='tag'),
    # path('search/', views.search, name='search'),
]
