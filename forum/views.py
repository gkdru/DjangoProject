from django.shortcuts import render
from .models import Post, Profile
from django.urls import reverse_lazy    
from django.http import HttpResponse    
from .forms import UserForm, ProfileForm, UserRegistrationForm
from django.views.generic import CreateView, ListView
from django.contrib.auth.decorators import login_required
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

class Profiles(ListView):
    model = Profile
    template_name = 'forum/profiles.html'
    context_object_name = 'profiles'

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        U_form = UserForm(request.POST, instance=request.user)
        P_form = ProfileForm(request.POST, instance=profile)
        password_form = PasswordChangeForm(request.user, request.POST)

        if U_form.is_valid() and P_form.is_valid() and password_form.is_valid():
            U_form.save()
            P_form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)
            return redirect('forum:profile')
    else:
        U_form = UserForm(instance=request.user)
        P_form = ProfileForm(instance=profile)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'forum/profile.html', {
        'U_form': U_form,
        'P_form': P_form,
        'password_form': password_form
    })
