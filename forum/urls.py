from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'forum'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='forum/forms/login.html', next_page='forum:index'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='forum/forms/logout.html',next_page='forum:index'), name='logout'),
    path('register/', views.register.as_view(), name='register'),
    # path('profile/', views.profile, name='profile'),
    # path('profile/edit/', views.edit_profile, name='edit_profile'),
    # path('profile/delete/', views.delete_profile, name='delete_profile'),
]
