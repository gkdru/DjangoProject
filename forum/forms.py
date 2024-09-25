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

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    image = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            try:
                user_profile = self.instance.profile
            except Profile.DoesNotExist:
                user_profile = None
            if user_profile:
                self.fields['image'].initial = user_profile.image

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            if self.cleaned_data.get('image'):
                profile.image = self.cleaned_data['image']
                profile.save()
        return user