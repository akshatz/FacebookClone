from auth_mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from blog.models import Posts
from django_project.settings import AUTH_USER_MODEL


class Friend(models.Model, LoginRequiredMixin):
    status = models.CharField(max_length=10)
    from_user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'from_user')
    to_user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="to_user")
    date_modified = models.DateTimeField(auto_now=True, null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def create(self,request, **kwargs):
        friend = self.create(from_user_id=request.user.id, status="pending")
        return friend

    class Meta:
        unique_together = (('from_user', 'to_user'),)

    def __str__(self):
        return self.to_user.email


class Share(models.Model):
    from_user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friend_user')
    to_user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='logged_in_user')
    shared_content = Posts.objects.all()
    is_friend = models.BooleanField(default=False)
