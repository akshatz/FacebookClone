from django.conf.urls import url
from django.urls import path, include, re_path

from friend import views
from .views import *

urlpatterns = [
    path('<int:pk>/', add_friend, name='addfriend'),
    url(r'^add_friend_link/(?P<uidb64>[0-9A-Za-z_\-]+)/$', add_friend_link, name='add_friend_link'),
    re_path(r'^accept_friend_request/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<status>[\w-]+)/$', accept_friend_request,
            name='accept_friend_request'),
    path('list/', friend_list, name='status'),
]