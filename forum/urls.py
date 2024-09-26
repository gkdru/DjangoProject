from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'forum'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='forum/forms/login.html', next_page='forum:index'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='forum/forms/logout.html', next_page='forum:index'), name='logout'),
    path('register/', views.register, name='register'),
    path('profiles/', views.profiles, name='profiles'),
    path('profile/<int:pk>/', views.my_profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
]
