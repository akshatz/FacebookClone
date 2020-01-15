from django.conf.urls import url
from django.urls import path, include
from .views import *

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('search/', search, name='friends_search'),
    path('profile/<int:pk>', profile_detail, name='profile'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate_account, name='activate'),

]
