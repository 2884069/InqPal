import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','inqpal_project.settings')

import django
django.setup()
from inqpal.models import Account,Post,Comment
from django.contrib.auth.models import User

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
         'picture':None},
         {'username':'DinoFLAME',
         'password':'coolK!d',
         'email':'Aoife@Campbell.com',
         'first_name':'Aoife',
         'last_name':'Campbell',
         'fav_dino':'Triceratops',
         'picture':None},
         {'username':'ROR',
         'password':'RoarOmegaRoar',
         'email':'monster@university.com',
         'first_name':'Richard',
         'last_name':'White',
         'fav_dino':'Spinosaurus',
         'picture':None}
    ]

    # add accounts
    for account in accounts:
        a = add_account(account['username'],account['password'],account['email'],account['first_name'],account['last_name'],account['fav_dino'],account['picture'])
        print("Account added: " + a)
        added_accounts.append(a)


    post_one_comments = [
        {'creator': added_accounts[1],
         'text':'old news'},
        {'creator': added_accounts[2],
         'text':'that ROCKS!'}
    ]

    post_two_comments = [{'creator':added_accounts[0],
                          'text':'definitely Nessie'}
    ]
    
    posts = [{'creator':added_accounts[0],'text':'I <3 deinonychus','category':'Theropods','comments':post_one_comments},
             {'creator':added_accounts[2],'text':'Mosasaurus goes hard','category':'Reptiles','comments':post_two_comments},
             {'creator':added_accounts[1],'text':'crocodile .o.','category':'Archosaurs','comments':[]}
    ]
    
    # adds posts, comments from posts
    for post in posts:
        p = add_post(post['creator'],post['text'],post['category'])
        for comment in post['comments']:
            add_comment(p, comment['creator'], comment['text'])

    # print out added posts
    for p in Post.objects.all():
        print(f'Post ' + p + ":")
        for c in Comment.objects.filter(post=p):
            print(f'- {c}')

def add_comment(post,creator,text):
    p = Comment.objects.get_or_create(post=post,creator=creator,text=text)[0]
    p.save()
    return p
    
def add_post(creator,text,category,image=None):
    c = Post.objects.get_or_create(creator=creator,text=text,category=category,image=image)[0]
    c.save()
    return c

def add_account(username,password,email,first_name,last_name,fav_dino,picture):
    u = User.objects.get_or_create(username=username,password=password,email=email,first_name=first_name,last_name=last_name)[0]
    u.save()
    a = Account.objects.get_or_create(user=u,fav_dino=fav_dino,picture=picture)[0]
    a.save()
    return a
    
# Start!
if __name__ == '__main__':
    print('Populating InqPal...')
    populate()