from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    POST_MAX_LEN = 2000

    # id?
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=POST_MAX_LEN)
    image = models.ImageField(upload_to='post_images', blank=True)
    # category = 
    # number_roars = models.IntegerField(default=0)
    # roar relation (M:N)

    def __str__(self):
        # should get some unique identifier
        return self.id

class Comment(models.Model):
    COMMENT_MAX_LEN = 500

    # id? if so based off Post id
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=COMMENT_MAX_LEN)

    def __str__(self):
        # should get some unique identifier
        return self.id
    
# class Account(models.Model):
# implementation varies depending on how we decide on doing it
# currently above assume utilising built-in django user