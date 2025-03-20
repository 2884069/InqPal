from django import forms
from django.contrib.auth.models import User
from inqpal.models import Account, Post,Comment
from django.contrib.auth.password_validation import validate_password
import datetime

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form' }),
                                help_text='Your password can not be too similar to your private information.')
    confirmation_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form' }),
                                            help_text='Enter the same password as before for verification.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirmation_password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form', 'placeholder': 'username'}),
            'email': forms.EmailInput(attrs={'class': 'form', 'placeholder': 'examplel@gmail.com'}),
            'password': forms.PasswordInput(attrs={'class': 'form'}),
            'confirmation_password': forms.PasswordInput(attrs={'class': 'form'})
        }
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'formPart'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'

        self.fields['password'].validators.append(validate_password)

    def clean_password_confirmation(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get("password")
        confirmation_password = cleaned_data.get("confirmation_password")

        if password and confirmation_password and password != confirmation_password:
            raise forms.ValidationError("The passwords you entered do not match.")
        
        return confirmation_password

class AccountForm(forms.ModelForm):
    fav_dino = forms.CharField(widget=forms.TextInput(attrs={'class': 'form'}))
    class Meta:
        model = Account
        fields = ('fav_dino', 'picture')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text',)

class CommentForm(forms.ModelForm):
    text = forms.CharField(label='Comment:',widget=forms.TextInput(attrs={"class": "form_field",'rows': 2}))
    class Meta:
        model = Comment
        fields = ('text',)
        
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('fav_dino', 'picture')
