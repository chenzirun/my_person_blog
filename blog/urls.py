
from django.urls import path, include
from . import views

app_name = 'blog'
urlpatterns = [
    path('index', views.IndexView.as_view(), name='index' ),
    path('detail/<int:id>', views.detail, name='detail'),
    path('archives/<int:year>/<int:month>', views.ArchivesView.as_view(), name='archives'),
    path('category/<int:id>', views.CategoryView.as_view(), name='category'),
]