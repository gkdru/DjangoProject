from django.shortcuts import render
from .models import User
from .models import Post
from django.urls import reverse_lazy    
from django.http import HttpResponse    
from .forms import UserForm
from django.views.generic import CreateView
# Create your views here.
def index(request):
    return HttpResponse('Hello World')
    # return render(request, 'forum/index.html')


class register(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('login')
    template_name = 'forum/forms/register.html'


