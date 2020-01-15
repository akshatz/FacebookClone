from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Posts)
# admin.site.register(Friend)