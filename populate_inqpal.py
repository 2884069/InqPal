import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','inqpal_project.settings')

import django
django.setup()
from inqpal.models import Account,Post,Comment
from django.contrib.auth.models import User
import datetime

def populate():

    # To make: 
    #   - Try creating and querying roars

    added_accounts = []

    accounts = [
        {'username':'Harvster',
         'password':'HarvestingHarves',
         'email':'harvey@harvey.com',
         'first_name':'Harvey',
         'last_name':'MacHarvey',
         'fav_dino':'Archaeopteryx',
         'picture':None
         },
        {'username':'DinoFLAME',
         'password':'coolK!d',
         'email':'Aoife@Campbell.com',
         'first_name':'Aoife',
         'last_name':'Campbell',
         'fav_dino':'Triceratops',
         'picture':None
         },
        {'username':'ROR',
         'password':'RoarOmegaRoar',
         'email':'monster@university.com',
         'first_name':'Richard',
         'last_name':'White',
         'fav_dino':'Spinosaurus',
         'picture':None
         }
    ]

    # add accounts
    a = None
    for account in accounts:
        a = add_account(account['username'],account['password'],account['email'],account['first_name'],account['last_name'],account['fav_dino'],account['picture'],a)
        print("Account added: " + a.__str__())
        added_accounts.append(a)


    post_one_comments = [
        {'creator': added_accounts[1],
         'text':'old news',
         'date':datetime.datetime(2025,1,23)},
        {'creator': added_accounts[2],
         'text':'that ROCKS!',
         'date':datetime.datetime(2025,2,13)}
    ]

    post_two_comments = [{'creator':added_accounts[0],
                          'text':'definitely Nessie',
                          'date':datetime.datetime(2025,2,23)}
    ]
    
    posts = [{'creator':added_accounts[0],'text':'I <3 deinonychus','category':'Theropods','comments':post_one_comments,'date':datetime.datetime(2025,1,5)},
             {'creator':added_accounts[2],'text':'Mosasaurus goes hard','category':'Reptiles','comments':post_two_comments,'date':datetime.datetime(2025,1,7)},
             {'creator':added_accounts[1],'text':'crocodile .o.','category':'Archosaurs','comments':[],'date':datetime.datetime(2025,3,13)}
    ]
    
    # adds posts, comments from posts
    for post in posts:
        p = add_post(post['creator'],post['text'],post['category'],post['date'])
        for comment in post['comments']:
            add_comment(p, comment['creator'], comment['text'],comment['date'])

    # print out added posts
    for p in Post.objects.all():
        print(f'Post ' + p.__str__() + ":")
        for c in Comment.objects.filter(post=p):
            print(f'- {c.__str__()}')

def add_comment(post,creator,text,date):
    p = Comment.objects.get_or_create(post=post,creator=creator,text=text,date=date)[0]
    p.save()
    return p
    
def add_post(creator,text,category,date,image=None):
    c = Post.objects.get_or_create(creator=creator,text=text,category=category,image=image,date=date)[0]
    c.save()
    return c

def add_account(username,password,email,first_name,last_name,fav_dino,picture,friend):
    u = User.objects.get_or_create(username=username,password=password,email=email,first_name=first_name,last_name=last_name)[0]
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