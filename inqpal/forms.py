from django.contrib.auth.models import User
from rango.models import Account

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', )

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('fav_dino', 'picture',)