import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','inqpal_project.settings')

import django
django.setup()
from inqpal.models import Account,Post,Comment,Category
from django.contrib.auth.models import User
import datetime

def check_if_none(str):
    if str == "None":
        return None
    return str

def read_comments(filename,added_accounts):
    comments = []
    if check_if_none(filename) != None:
        with open(os.path.join("population_files",filename)) as f:
            for line in f:
                comment_details = line.split(',')
                comments.append({
                    'creator':added_accounts[int(comment_details[0].strip())],
                    'text':comment_details[1].strip().replace("*",","),
                    'date':datetime.datetime.strptime(comment_details[2].strip(),'%Y %m %d')
                })
    return comments

def populate():

    # To make: 
    #   - Try creating and querying roars

    added_accounts = []

    # read accounts
    accounts = []
    with open(os.path.join("population_files","accounts.csv")) as f:
        for line in f:
            account_details = line.split(',')
            accounts.append({
                'username':account_details[0].strip(),
                'password':account_details[1].strip(),
                'email':account_details[2].strip(),
                'first_name':account_details[3].strip(),
                'last_name':account_details[4].strip(),
                'fav_dino':account_details[5].strip(),
                'picture':check_if_none(account_details[6].strip())
            })

    # add accounts
    a = None
    for account in accounts:
        a = add_account(account['username'],account['password'],account['email'],account['first_name'],account['last_name'],account['fav_dino'],account['picture'],a)
        print("Account added: " + a.__str__())
        added_accounts.append(a)

    # read categories
    categories = []
    with open(os.path.join("population_files","categories.csv")) as f:
        for line in f:
            category_details = line.split(',')
            categories.append({
                'name':category_details[0].strip(),
                'text':category_details[1].strip().replace("*",","),
                'image':check_if_none(category_details[2].strip())
            })

    # add categories
    for cat in categories:
        c = add_category(cat['name'],cat['text'],cat['image'])

    # read posts and comments
    posts = []
    with open(os.path.join("population_files","posts.csv")) as f:
        for line in f:
            post_details = line.split(',')
            posts.append({
                'creator':added_accounts[int(post_details[0].strip())],
                'text':post_details[1].strip().replace("*",","),
                'category':post_details[2].strip(),
                'comments':read_comments(post_details[3].strip(),added_accounts),
                'date':datetime.datetime.strptime(post_details[4].strip(),'%Y %m %d'),
                'image':check_if_none(post_details[5].strip())
            })
    
    # add posts and comments
    for post in posts:
        p = add_post(post['creator'],post['text'],post['category'],post['date'],post['image'])
        for comment in post['comments']:
            add_comment(p, comment['creator'], comment['text'],comment['date'])

    # print out added posts
    for p in Post.objects.all():
        print(f'Post ' + p.__str__() + ":")
        for c in Comment.objects.filter(post=p):
            print(f'- {c.__str__()}')

def add_comment(post,creator,text,date):
    c = Comment.objects.get_or_create(post=post,creator=creator,text=text,date=date)[0]
    c.save()
    return c
    
def add_post(creator,text,category,date,image=None):
    category = Category.objects.get(name=category)
    p = Post.objects.get_or_create(creator=creator,text=text,category=category,image=image,date=date)[0]
    p.save()
    return p

def add_category(name,description,picture):
    c = Category.objects.get_or_create(name=name,description=description,picture=picture)[0]
    c.save()
    return c

def add_account(username,password,email,first_name,last_name,fav_dino,picture,friend):
    u = User.objects.get_or_create(username=username,password=password,email=email,first_name=first_name,last_name=last_name)[0]
    u.set_password(u.password)
    u.save()
    a = Account.objects.get_or_create(user=u,fav_dino=fav_dino,picture=picture)[0]
    if friend != None:
        a.friends.add(friend)
    a.save()
    return a
    
# Start!
if __name__ == '__main__':
    print('Populating InqPal...')
    populate()