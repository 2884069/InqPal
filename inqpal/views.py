from inqpal import models
from inqpal.models import Account,Comment,Post,Category
from inqpal.forms import PostForm, UserForm, AccountForm, CommentForm, EditProfileForm

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from inqpal.forms import PostForm, UserForm, AccountForm
from django.contrib import messages
import datetime
from django.template.loader import render_to_string
import math
from django.core.paginator import Paginator


POSTS_PER_PAGE = 10

def handle_comment_form_post(request):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = Post.objects.get(id=request.POST.get('post'))
        comment.creator = request.user.account
        comment.date = datetime.datetime.now()
        comment.save()
    else:
        print(comment_form.errors)

def handle_comment_delete_post(request):
    Comment.objects.get(id=request.POST.get('comment')).delete()

def handle_roar_form_post(request):
    post = Post.objects.get(id=request.POST.get('post'))
    post.roars.add(request.user.account)

def handle_unroar_form_post(request):
    post = Post.objects.get(id=request.POST.get('post'))
    post.roars.remove(request.user.account)

def index(request):
    if request.user.is_authenticated:
        return redirect('inqpal:palsposts')
    else:
        return redirect('inqpal:trending')

def trending(request,page=1):
    page -= 1
    context_dict = {}
    form = CommentForm()
    context_dict['form'] = form
    context_dict['logged_in'] = request.user.is_authenticated

    if request.method == "POST":
        if request.POST.get('submit') == 'post':
            handle_comment_form_post(request)
        elif request.POST.get('submit') == 'delete':
            handle_comment_delete_post(request)
        elif request.POST.get('submit') == 'roar':
            handle_roar_form_post(request)
        elif request.POST.get('submit') == 'unroar':
            handle_unroar_form_post(request)
    
    context_dict['type'] = 'Trending'
    context_dict['this_url'] = reverse('inqpal:trending')

    number_of_pages = math.ceil(Post.objects.all().count()/POSTS_PER_PAGE)
    if (number_of_pages > 0):
        pages = [{'page_number':x,'page_link':reverse('inqpal:trending', kwargs={'page':x})} for x in range(1,number_of_pages+1)]
        pages[page]['this'] = True
        context_dict['pages'] = pages

    post_list = Post.objects.annotate(num_roars=Count("roars")).order_by("-num_roars")[POSTS_PER_PAGE*page:POSTS_PER_PAGE*(page+1)]
    if context_dict['logged_in']:
        post_list = [{'post':p,'roars':p.roars.count,'comments':[{'comment':c,'mine':c.creator == request.user.account} for c in Comment.objects.filter(post=p).order_by('date')]} for p in post_list]
    else:
        post_list = [{'post':p,'roars':p.roars.count,'comments':[{'comment':c} for c in Comment.objects.filter(post=p).order_by('date')]} for p in post_list]
    
    # if logged in, checks which posts you've already roared
    if request.user.is_authenticated:
        account = request.user.account
        for p in post_list:
            if p['post'].roars.filter(id=account.id).exists():
                p['roared'] = True

    context_dict['posts'] = post_list
    return render(request, 'inqpal/display_posts.html', context=context_dict)

@login_required
def pals_posts(request,page=1):
    page -= 1
    context_dict = {}
    form = CommentForm()
    context_dict['form'] = form
    context_dict['logged_in'] = True

    if request.method == "POST":
        if request.POST.get('submit') == 'post':
            handle_comment_form_post(request)
        elif request.POST.get('submit') == 'delete':
            handle_comment_delete_post(request)
        elif request.POST.get('submit') == 'roar':
            handle_roar_form_post(request)
        elif request.POST.get('submit') == 'unroar':
            handle_unroar_form_post(request)
    
    context_dict['type'] = 'Pals Posts'
    context_dict['this_url'] = reverse('inqpal:palsposts')

    user = request.user
    account = Account.objects.get(user=user)

    number_of_pages = math.ceil(Post.objects.filter(creator__in=account.friends.all()).count()/POSTS_PER_PAGE)
    if (number_of_pages > 0):
        pages = [{'page_number':x,'page_link':reverse('inqpal:palsposts', kwargs={'page':x})} for x in range(1,number_of_pages+1)]
        pages[page]['this'] = True
        context_dict['pages'] = pages

    post_list = Post.objects.filter(creator__in=account.friends.all()).annotate(num_roars=Count("roars")).order_by("-num_roars")[POSTS_PER_PAGE*page:POSTS_PER_PAGE*(page+1)]
    if context_dict['logged_in']:
        post_list = [{'post':p,'roars':p.roars.count,'comments':[{'comment':c,'mine':c.creator == request.user.account} for c in Comment.objects.filter(post=p).order_by('date')]} for p in post_list]
    else:
        post_list = [{'post':p,'roars':p.roars.count,'comments':[{'comment':c} for c in Comment.objects.filter(post=p).order_by('date')]} for p in post_list]
    
    # Checks which posts you've already roared
    for p in post_list:
        if p['post'].roars.filter(id=account.id).exists():
            p['roared'] = True
    
    context_dict['posts'] = post_list
    return render(request, 'inqpal/display_posts.html', context=context_dict)

def categories(request):
    context_dict = {}
    categories = Category.objects.all()
    categories = [{"category":x,"posts":Post.objects.filter(category=x).count()} for x in categories]
    context_dict["categories"] = categories
    return render(request,'inqpal/display_categories.html',context=context_dict)

def show_category(request,category_name,page=1):
    page -= 1
    context_dict = {}
    form = CommentForm()
    context_dict['form'] = form
    context_dict['logged_in'] = request.user.is_authenticated

    if request.method == "POST":
        if request.POST.get('submit') == 'post':
            handle_comment_form_post(request)
        elif request.POST.get('submit') == 'delete':
            handle_comment_delete_post(request)
        elif request.POST.get('submit') == 'roar':
            handle_roar_form_post(request)
        elif request.POST.get('submit') == 'unroar':
            handle_unroar_form_post(request)
    
    context_dict['type'] = category_name
    context_dict['this_url'] = reverse('inqpal:show_category', kwargs={'category_name':category_name})

    number_of_pages = math.ceil(Post.objects.filter(category=Category.objects.get(name=category_name)).count()/POSTS_PER_PAGE)
    if (number_of_pages > 0):
        pages = [{'page_number':x,'page_link':reverse('inqpal:show_category', kwargs={'category_name':category_name,'page':x})} for x in range(1,number_of_pages+1)]
        pages[page]['this'] = True
        context_dict['pages'] = pages

    post_list = Post.objects.filter(category=Category.objects.get(name=category_name)).annotate(num_roars=Count("roars")).order_by("-num_roars")[POSTS_PER_PAGE*page:POSTS_PER_PAGE*(page+1)]
    if context_dict['logged_in']:
        post_list = [{'post':p,'roars':p.roars.count,'comments':[{'comment':c,'mine':c.creator == request.user.account} for c in Comment.objects.filter(post=p).order_by('date')]} for p in post_list]
    else:
        post_list = [{'post':p,'roars':p.roars.count,'comments':[{'comment':c} for c in Comment.objects.filter(post=p).order_by('date')]} for p in post_list]
    
    # if logged in, checks which posts you've already roared
    if context_dict['logged_in']:
        account = request.user.account
        for p in post_list:
            if p['post'].roars.filter(id=account.id).exists():
                p['roared'] = True
    
    context_dict['posts'] = post_list
    return render(request, 'inqpal/display_posts.html', context=context_dict)

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
            return redirect('inqpal:my_account')
        
        else:
            messages.error(request, 'registration failed. Please try again.')
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

@login_required
def my_account(request):
    user = request.user
    try:
        account = Account.objects.get(user=user)
    except ObjectDoesNotExist:
        messages.error(request, "Your account profile does not exist. Please complete your registration.")
        return redirect(reverse('inqpal:register'))
    
    all_posts = Post.objects.filter(creator=account).order_by('-date')
    paginator = Paginator(all_posts, 3)
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)
    
    if request.method == "POST":
        selected_posts = request.POST.getlist('selected_posts')
        Post.objects.filter(id__in=selected_posts).delete()
        messages.success(request, "Selected posts deleted successfully.")
        return redirect(reverse('inqpal:my_account'))
    
    context = {
        'account': account,
        'posts': posts,
        'posts_count': account.posts_count(),
        'friends': account.friends_count(),
        'watchers': account.watchers_count(),
    }
    return render(request, 'inqpal/my_account.html', context)

@login_required
def make_post(request):
    failure = False

    if request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            if 'image' in request.FILES and 'category' in request.POST:
                post = post_form.save(commit = False)
                post.image = request.FILES['image']
                post.creator = request.user.account
                post.category = Category.objects.get(name = request.POST['category'])
                post.date = datetime.date.today()
                post.save()
                return redirect(reverse('inqpal:my_account'))
            else:
                failure = True

        else:
            print(post_form.errors)
            failure = True
    
    else:
        post_form = PostForm()
    

    return render(request, 'inqpal/make_post.html', context= {'username' : str(request.user.account), 'failure': failure})


@login_required
def edit_profile(request):
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance = request.user.account)
        if form.is_valid():
            form.save()
            return redirect(reverse('inqpal:my_account'))
        else:
            print(form.errors)
    else:
        form = EditProfileForm(instance = request.user.account)
    return render(request, 'inqpal/edit_profile.html', context = {'form': form})
        
        

@login_required
def add_pal(request):
    ctx = {'users_friends': [[],[]]}
    search_parameter = request.GET.get("q")

    if search_parameter:
        users_friends = Account.objects.filter(user__username__icontains=search_parameter).exclude(user__id = request.user.id).filter(user__id__in= request.user.account.friends.all())
        users_not_friends = Account.objects.filter(user__username__icontains=search_parameter).exclude(user__id = request.user.id).exclude(user__id__in= request.user.account.friends.all())
    else:
        users_friends = Account.objects.exclude(user__id = request.user.id).filter(user__id__in= request.user.account.friends.all())
        users_not_friends = Account.objects.exclude(user__id = request.user.id).exclude(user__id__in= request.user.account.friends.all())
    
    ctx["users_friends"][0] = users_not_friends
    ctx["users_friends"][1] = users_friends

    matches = len(users_friends) + len(users_not_friends)
    if matches <= 0:
        ctx['number_of_matches'] = 'No'
    else:
        ctx['number_of_matches'] = str(matches)

    if matches == 1:
        ctx['number_of_matches'] += ' Match'
    else:
        ctx['number_of_matches'] += ' Matches'
    


    if request.method == 'POST':
        current_account = request.user.account
        try:
            pal = Account.objects.get(user__id = request.POST.get('pal_id'))
        except Account.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'}, status=400)
        do = request.POST.get('do')

        if do == 'Watch':
            current_account.friends.add(pal)
        elif do == 'Unwatch':
            current_account.friends.remove(pal)
        else:
            return JsonResponse({'success': False, 'error': 'invalid operation please reload page'}, status=400)

        current_account.save()
        return JsonResponse({'success':True})


    is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest"
    if is_ajax_request:
        html = render_to_string("inqpal/add_pal_results.html", ctx)
        data_dict = {'html_from_view': html}
        return JsonResponse(data_dict, safe=False)

    return render(request, 'inqpal/add_pal.html', context=ctx)