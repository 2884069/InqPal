from django.shortcuts import render
from django.contrib.auth.models import User
from rango.models import Account


def index(request):
    pass

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

def login(request):
    pass

def my_account(request):
    pass

def make_post(request):
    pass

def edit_profile(request):
    pass

def add_pal(request):
    pass