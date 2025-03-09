from django import forms
from django.contrib.auth.models import User
from inqpal.models import Account

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    #confirm_password = forms.CharField(widget=forms.PasswordInput())

        # if password != confirm_password:
        #     raise forms.ValidationError("Passwords do not match.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('fav_dino', 'picture')