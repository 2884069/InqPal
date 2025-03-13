from django.shortcuts import render
from django.contrib.auth.models import User
from inqpal import models
<<<<<<< Updated upstream
from inqpal.models import Account,Comment,Post
from django.contrib.auth import authenticate, login
=======
from inqpal.models import Account
from django.contrib.auth import authenticate, login, logout
>>>>>>> Stashed changes
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from inqpal.forms import PostForm, UserForm, AccountForm
from django.contrib import messages

POSTS_PER_PAGE = 10

def index(request):
    return render(request, 'inqpal/base.html', context = {})

def trending(request):
    context_dict = {}

    post_list = Post.objects.order_by('-roars')[:POSTS_PER_PAGE]
    post_list = [{'post':p,'roars':p.roars.count,'comments':Comment.objects.filter(post=p).order_by('date')} for p in post_list]
    context_dict['posts'] = post_list

    return render(request, 'inqpal/display_posts.html', context=context_dict)

@login_required
def palsposts(request):
    pass

def categories(request):
    pass

def show_category(request):
    pass

def signup(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(request.POST)
        account_form = AccountForm(request.POST)

        if user_form.is_valid() and account_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            account = account_form.save(commit=False)
            account.user = user

            if 'picture' in request.FILES:
                account.picture = request.FILES['picture']
            
            account.save()
            registered = True
            messages.success(request, 'You have successfully registered! You can now log in.')

            login(request, user)
            return redirect(reverse('inqpal:my_account'))
        
        else:
            messages.error(request, 'registration failed. Pleasde try again.')
            print(user_form.errors, account_form.errors)
        
    else:
        user_form = UserForm()
        account_form = AccountForm()

    return render(request, 'inqpal/register.html', context = {'user_form': user_form, 'account_form': account_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect(reverse('inqpal:my_account'))
            else:
                return HttpResponse("Your InqPal account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    
    return render(request, 'inqpal/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('inqpal:index'))

def my_account(request):
    user = request.user
    account = Account.objects.get(user=user)
    context = {
        'account': account,
        'friends': account.friends_count(),
        'watchers': account.watchers_count(),
    }
    return render(request, 'inqpal/account.html', context)

@login_required
def make_post(request):

    if request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid:
            post = post_form.save(commit = False)
            post.image = request.FILES['image']
            post.creator = request.user.account
            post.save()

        else:
            print(post_form.errors)
    
    else:
        post_form = PostForm()
    
    return render(request, 'inqpal/make_post.html', context= {'username' : str(request.user.account)})


@login_required
def edit_profile(request):
    pass

#removed for testing purposes
#@login_required
def add_pal(request):
    accounts = []
    def name_contains(account):
        return str(account) == search_name
    
    if 'search' in request.GET:
        search_name = request.GET['search']
        accounts = filter(name_contains, Account.objects.all())
        return render(request, 'inqpal/add_pal.html', context= {'accounts' : accounts})
    return render(request, 'inqpal/add_pal.html')