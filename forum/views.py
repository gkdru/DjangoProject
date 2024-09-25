from django.shortcuts import render, redirect
from .models import Post, Profile
from django.urls import reverse    
from django.http import HttpResponse    
from .forms import UserForm, ProfileForm, UserRegistrationForm, UserProfileForm
from django.views.generic import ListView
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
    return render(request, 'forum/index.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('forum:profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'forum/forms/register.html', {'form': form})


def profiles(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.all()
        context = {'profiles': profiles}
    else:
        messages.warning(request, 'Вы должны войти в систему, чтобы просмотреть профили!')
        context = {}
    
    return render(request, 'forum/profiles.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        if 'password_change' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('forum:profile')
        else:
            user_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('forum:profile')
    else:
        user_form = UserProfileForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
    
    return render(request, 'forum/profile.html', {
        'user_form': user_form,
        'password_form': password_form
    })