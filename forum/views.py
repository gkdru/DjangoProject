from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Profile, Comment
from .forms import UserRegistrationForm, UserProfileForm, CommentForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth import login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import update_session_auth_hash




# Create your views here.
def index(request):
    posts = Post.objects.all().order_by('-created_at')

    return render(request, 'forum/index.html', {'posts': posts})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('forum:profile', pk=user.pk)  # Передаем pk нового пользователя
    else:
        form = UserRegistrationForm()
    return render(request, 'forum/forms/register.html', {'form': form})


def profiles(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.all()
        context = {'profiles': profiles}
    else:
        messages.warning(request, 'Вы должны войти в систему, чтобы просмотреть профили!')
        return redirect('forum:index')
    
    return render(request, 'forum/profiles.html', context)

def my_profile(request, pk):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user_id=pk)
        posts = Post.objects.filter(author=profile.user).order_by('-created_at')
        context = {'profile': profile, 'posts': posts}
    else:
        messages.warning(request, 'Вы должны войти в систему, чтобы просмотреть профиль!')
        return redirect('forum:index')

    return render(request, 'forum/profile.html', context) 

@login_required
def edit_profile(request):
    if request.method == 'POST':
        if 'password_change' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('forum:profile', pk=request.user.pk)  # Передаем pk текущего пользователя
        else:
            user_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('forum:profile', pk=request.user.pk)  # Передаем pk текущего пользователя
    else:
        user_form = UserProfileForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
    
    return render(request, 'forum/edit_profile.html', {
        'user_form': user_form,
        'password_form': password_form
    })


def post_detail(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.all()
        new_comment = None

        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.author = request.user
                new_comment.save()
                return redirect('forum:post_detail', pk=post.pk)
        else:
            comment_form = CommentForm()

        return render(request, 'forum/post_detail.html', {
            'post': post,   
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form    
        })
    else:
        messages.warning(request, 'Вы должны войти в систему, чтобы просмотреть пост!')
        return redirect('forum:index')


def create_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('forum:post_detail', pk=post.pk)
        else:
            form = PostForm()
    else:
        messages.warning(request, 'Вы должны войти в систему, чтобы создать пост!')
        return redirect('forum:index')
    return render(request, 'forum/create_post.html', {'form': form})