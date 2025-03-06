import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','inqpal_project.settings')

import django
django.setup()
from inqpal.models import Account,Post,Comment
from django.contrib.auth.models import User

def populate():

    # To make: 
    #   - Account adder
    #   - Tie Posts + Comments to Accounts
    #   - Try creating and querying roars

    post_one_comments = [
        {'creator': None,
         'text':'Very cool!'},
        {'creator':None,
         'text':'that ROCKS!'}]

    post_two_comments = [{'creator':None,
                          'text':'definitely Nessie'}]
    
    posts = [{'creator':None,'text':'I <3 deinonychus','category':'Theropods','comments':post_one_comments},
             {'creator':None,'text':'Mosasaurus goes hard','category':'Reptiles','comments':post_two_comments},
             {'creator':None,'text':'crocodile .o.','category':'Archosaurs','comments':[]}]
    
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
    
# Start!
if __name__ == '__main__':
    print('Populating InqPal...')
    populate()