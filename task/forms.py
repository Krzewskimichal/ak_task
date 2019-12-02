from django import forms
from task.models import PostModel, CommentModel


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=128, required=True, label='username')
    password1 = forms.CharField(widget=forms.PasswordInput, required=True, label='password')
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, label='reapit password')
    email = forms.EmailField(required=True, label='email')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128, label='username', required=True, widget=forms.TextInput)
    password = forms.CharField(required=True, label='password', widget=forms.PasswordInput)


class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['title', 'content']
