from django.contrib.auth.models import User

from django import forms

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Comment, Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'short_description', 'full_description', 'photo', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title of an article'
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Short description...',
                'rows': 3
            }),
            'full_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Full description...',
                'rows': 3
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            })
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your comment'
            })
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))

    class Meta:
        model = User


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm your password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name'
            }),
        }