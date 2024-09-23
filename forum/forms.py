from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        error_messages = {
            'username': {
                'required': 'Please enter your username',
            },
            'password1': {
                'required': 'Please enter your password',
            },
            'password2': {
                'required': 'Please confirm your password',
            },
        }
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = self.fields['email'].label or 'Write your email'
        self.fields['username'].widget.attrs['placeholder'] = self.fields['username'].label or 'Write your username'
        self.fields['password1'].widget.attrs['placeholder'] = self.fields['password1'].label or 'Write your password'
        self.fields['password2'].widget.attrs['placeholder'] = self.fields['password2'].label or 'Confirm your password'        
