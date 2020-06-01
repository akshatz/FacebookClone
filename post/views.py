from django.contrib import messages
from django.urls import reverse_lazy
from django_project.settings import AUTH_USER_MODEL as model
from .models import Post
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django_project.settings import MEDIA_URL
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from friend.models import Friend, Share
from django.db.models import Q
user = get_user_model()
from django.core.paginator import Paginator

@login_required
def home_view(request):
    """Display all the post of friends and own posts on the dashboard"""
    # post = Post.objects.filter(Q(author=request.user) | Q(author__from_user=request.user) | Q(author__to_user=request.user)).order_by('-date_posted')
    post = Post.objects.all().order_by('-date_modified')
    media = MEDIA_URL
    paginator = Paginator(post, 2) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'post/home.html', {'page_obj': page_obj, 'post':post, 'media':MEDIA_URL})
    
class PostDetailView(DetailView):
    """Options to Update, delete the post"""
    if user.is_authenticated:
        model = Post
        success_url = 'post/home.html'
    else:
        redirect('/post')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-date_modified')

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
    model = Post
    success_url = '/post/'

    def form_valid(self, form):
        try:
            form.instance.author = self.request.user
            return super(PostCreateView, self).form_valid(form)
        except:
            return redirect(reverse_lazy('post'))


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Post update form  has fields
        title
        content
        image
        video
    """

    model = Post
    fields = ['title', 'content', 'image', 'video']
    success_url = '/post/'

    def form_valid(self, form):
        try:
            form.instance.author = self.request.user
            super(PostUpdateView, self).form_valid(form)
            messages.success(self.request, 'You have successfully updated the post')
            return redirect(reverse_lazy('post-update', kwargs={'pk': self.object.uuid}))
        except:
            pass
            messages.error(self.request, 'You cannot update the post. Please retry!!!')
            return redirect(reverse_lazy('post-update', kwargs={'pk': self.object.uuid}))

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Deletion of the post"""
    model = Post
    success_url = '/post'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# def about(request):
#     """About page forthe company"""
#     return render(request, 'post/about.html', {'title': 'About'})


class UserPostListView(ListView):
    """Own post and friend post are visible"""
    model = Post
    template_name = 'post/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-date_modified']

    def get_queryset(self):
        user = get_object_or_404(model, username=self.kwargs.get('pk'))
        return Post.objects.all().order_by('-date_posted')
