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

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmation_password = cleaned_data.get("confirmation_password")

        if password and confirmation_password and password != confirmation_password:
            self.add_error('confirmation_password', "The passwords you entered do not match.")
        
        return cleaned_data

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
    
    picture = forms.ImageField(required=False)
    
    def clean_picture(self):
        picture = self.cleaned_data.get('picture')
        if picture:
            allowed_image_types = ['image/jpeg', 'image/png', 'image/gif']
            if hasattr(picture, 'content_type') and picture.content_type not in allowed_image_types:
                raise forms.ValidationError("Only JPG, PNG and GIF images are allowed")
        
            maximum_size = 10 * 1024 * 1024
            if picture.size > maximum_size:
                raise forms.ValidationError("Image is too large, it has to be less than 10MB")
        return picture
        
        
            
