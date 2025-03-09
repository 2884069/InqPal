from django.shortcuts import render
from django.contrib.auth.models import User
from inqpal.models import Account
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, 'inqpal/base.html', context = {})

def trending(request):
    pass

def palsposts(request):
    pass

def categories(request):
    pass

def show_category(request):
    pass

def signup(request):
    register = False

    if request.method == "POST":
        user_form = UserForm(request.POST)
        account_form = AccountForm(request.POST)

        if user_form.is_valid() and account_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            account = account_form.save(commit=False)
            account.user = user

            if 'picture' in request.FILES:
                account.picture = request.FILES['picture']
            
            account.save()
            registred = True
        
        else:
            print(user_form.errors, account_form.errors)
        
    else:
        user_form = UserForm()
        account_form = AccountForm()

    return render(request, 'inqpal/register.html', context = {'user_form': user_form, 'account_form': account_form, 'registered': registred})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your InqPal account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    
    else:
        return render(request, 'inqpal/login.html')


def my_account(request):
    pass

@login_required
def make_post(request):
    pass

def edit_profile(request):
    pass

@login_required
def add_pal(request):
    pass