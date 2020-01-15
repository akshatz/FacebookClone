from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from PIL import Image
from django_project.settings import AUTH_USER_MODEL
import uuid


class User(AbstractUser):
    """
        Custom User model will be having user id as primary key, first_name, last_name and username
        will be imported from AbstractUser model
        Date of birth for entering date of birth
    """
    email = models.EmailField(max_length=255, unique=True)
    dateofbirth = models.DateField(null=True)
    # friend_id = models.ManyToManyField('self')
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Posts(models.Model):
    """
    Post has
    title,
    content,
    image,
    video
    """

    title = models.CharField(max_length=100, verbose_name="Title:")
    content = models.TextField(verbose_name="Content:")
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_pics", null=True, blank=True, verbose_name="Image:")
    date_modified = models.DateTimeField(auto_now=True, blank=True)
    video = models.FileField(upload_to='videos/',blank=True, null=True, verbose_name="video limited to mp4:")
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    draft = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


    def total_likes(self):
        return self.likes.count

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    @property
    def photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    # class PostManager(models.Manager):
    #     def active(self, *args, **kwargs):
    #         # Post.objects.all() = super(PostManager, self).all()
    #         return super(self, self).filter(draft=False).filter(publish__lte=timezone.now())



