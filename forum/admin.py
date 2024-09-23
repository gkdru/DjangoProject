from django.contrib import admin

# Register your models here.
from .models import User, Post, Profile

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'email', 'password']
    inlines = [ProfileInline]

admin.site.register(User, UserAdmin)
admin.site.register(Post)



