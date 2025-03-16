from django import forms
from django.contrib.auth.models import User
from inqpal.models import Account, Post,Comment
import datetime

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form'}))
    #confirm_password = forms.CharField(widget=forms.PasswordInput())

        # if password != confirm_password:
        #     raise forms.ValidationError("Passwords do not match.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form'}),
            'email': forms.EmailInput(attrs={'class': 'form'}),
            'password': forms.PasswordInput(attrs={'class': 'form'}),
        }

class AccountForm(forms.ModelForm):
    fav_dino = forms.CharField(widget=forms.TextInput(attrs={'class': 'form'}))
    class Meta:
        model = Account
        fields = ('fav_dino', 'picture')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'image', 'category')

class CommentForm(forms.ModelForm):
    text = forms.CharField(max_length=Comment.COMMENT_MAX_LEN,help_text="Comment Here")
    date = forms.IntegerField(widget=forms.HiddenInput(), initial=datetime.datetime.now())

    class Meta:
        model = Comment
        fields = ('text')