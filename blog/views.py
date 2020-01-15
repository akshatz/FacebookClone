import random

from django.contrib import messages
from django.core.handlers import exception
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.deprecation import MiddlewareMixin

from django_project.settings import AUTH_USER_MODEL
from friend.models import Friend
from .models import Posts
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django_project.settings import MEDIA_URL
from django.contrib.auth.decorators import login_required

user = get_user_model()


@login_required
def home_view(request):
    """Display all the post of friends and own posts on the dashboard"""
    if request.user.is_authenticated:
        context = {
            'posts': Posts.objects.filter(author=request.user).order_by('-date_posted'),
            'media': MEDIA_URL,
        }
        return render(request, 'blog/home.html', context)
    else:
        return render(request, 'users/login.html')


class PostDetailView(DetailView):
    """Options to Update, delete the post"""
    if user.is_authenticated:
        model = Posts
        success_url = 'blog/home.html'
    else:
        redirect('/blog')

    def get_queryset(self):
        return Posts.objects.filter(author=self.request.user).order_by('date_posted')

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self) \
            .get_context_data(**kwargs)
        context['media'] = MEDIA_URL
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
        Post form has fields
            title
            content
            image
            video
    """
    fields = ['title', 'content', 'image', 'video']
    model = Posts
    success_url = '/blog'

    def form_valid(self, form):
        try:
            form.instance.author = self.request.user
            return super(PostCreateView, self).form_valid(form)
        except:
            return redirect(reverse_lazy('home'))


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Post update form  has fields
        title
        content
        image
        video
    """
    model = Posts
    fields = ['title', 'content', 'image', 'video']
    success_url = '/blog'

    def form_valid(self, form):
        try:
            form.instance.author = self.request.user
            super(PostUpdateView, self).form_valid(form)
            messages.success(self.request, 'You have successfully updated the post')
            return redirect(reverse_lazy('post-update', kwargs={'pk': self.object.uuid}))
        except:
            messages.success(self.request, 'You have successfully updated the post')
            return redirect(reverse_lazy('post-update', kwargs={'pk': self.object.uuid}))

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Deletion of the post"""
    model = Posts
    success_url = '/blog'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# def about(request):
#     """About page forthe company"""
#     return render(request, 'blog/about.html', {'title': 'About'})


class UserPostListView(ListView):
    """Own post and friend blog are visible"""
    model = Posts
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-date_posted']

    def get_queryset(self):
        user = get_object_or_404(AUTH_USER_MODEL, username=self.kwargs.get('pk'))
        return Posts.objects.filter(author=user).order_by('-date_posted')
