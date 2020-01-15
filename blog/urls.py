from django.conf.urls import url
from django.urls import path, include

from .views import (
    home_view,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
)
from .views import *

urlpatterns = [
    path('', home_view, name='blog-home'),
    path('user/<int:pk>', UserPostListView.as_view(), name='user-posts'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    url('post/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', PostDetailView.as_view(), name='post-detail'),
    url('post/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/update', PostUpdateView.as_view(), name='post-update'),
    url('post/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/delete', PostDeleteView.as_view(), name='post-delete'),
    # path('about/', about, name='blog-about'),
    # url('likes/', like_post, name='likes_post'),
]
