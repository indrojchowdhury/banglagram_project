from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, UserProfile, Story

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add help text to fields
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        
        # Add styling
        self.fields['username'].widget.attrs.update({
            'class': 'w-full border rounded-xl px-4 py-3 bg-gray-50 focus:ring-2 focus:ring-blue-500 outline-none'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'w-full border rounded-xl px-4 py-3 bg-gray-50 focus:ring-2 focus:ring-blue-500 outline-none'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full border rounded-xl px-4 py-3 bg-gray-50 focus:ring-2 focus:ring-blue-500 outline-none'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full border rounded-xl px-4 py-3 bg-gray-50 focus:ring-2 focus:ring-blue-500 outline-none'
        })

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full border rounded-xl px-4 py-3 bg-gray-50 focus:ring-2 focus:ring-blue-500 outline-none'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full border rounded-xl px-4 py-3 bg-gray-50 focus:ring-2 focus:ring-blue-500 outline-none'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full border rounded-xl px-4 py-3 bg-gray-50 focus:ring-2 focus:ring-blue-500 outline-none'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full border rounded-xl px-4 py-3 bg-gray-50 focus:ring-2 focus:ring-blue-500 outline-none'
            }),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_pic']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'w-full border rounded-xl px-4 py-3 bg-gray-50 focus:ring-2 focus:ring-blue-500 outline-none',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'profile_pic': forms.FileInput(attrs={
                'class': 'w-full border rounded-xl px-4 py-3 bg-gray-50 focus:ring-2 focus:ring-blue-500 outline-none'
            })
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border rounded-xl px-4 py-3 bg-gray-50 focus:ring-2 focus:ring-blue-500 outline-none',
                'placeholder': 'Enter a catchy title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full border rounded-xl px-4 py-3 bg-gray-50 focus:ring-2 focus:ring-blue-500 outline-none',
                'rows': 6,
                'placeholder': 'What is on your mind?'
            }),
        }

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'w-full border rounded-xl px-4 py-3 bg-gray-50 focus:ring-2 focus:ring-blue-500 outline-none',
                'accept': 'image/*'
            })
        }