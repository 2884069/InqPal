from django import forms
from django.contrib.auth.models import User
from inqpal.models import Account, Post,Comment
import datetime

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form' }),
                                help_text='<p> Your password can not be too similar to your private information. </p>')
    confirmation_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form' }),
                                            help_text='<p> Enter the same password as before for verification. </p>')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirmation_password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form', 'placeholder': 'username'}),
            'email': forms.EmailInput(attrs={'class': 'form', 'placeholder': 'email@gmail.com'}),
            'password': forms.PasswordInput(attrs={'class': 'form'}),
            'confirmation_password': forms.PasswordInput(attrs={'class': 'form'})
        }
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'formPart'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<p> Required. 150 characters or fewer.Letters, digits and @/./+/-/_ only.</p>'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmation_password = cleaned_data.get("confirmation_password")

        if password and confirmation_password and password != confirmation_password:
            self.add_error('confirmation_password', "Passwords do not match.")

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
        fields = ('text','date','post')