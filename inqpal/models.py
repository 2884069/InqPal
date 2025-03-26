import os
from django.db import models
from django.contrib.auth.models import User
import datetime

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    friends = models.ManyToManyField('self',related_name='watchers',symmetrical=False,blank=True)
    fav_dino = models.CharField(max_length=50)
    picture = models.ImageField(default="noImageSelected.png", upload_to='profile_images', blank=True)
    def __str__(self):
        return self.user.username
    
    def friends_count(self):
        return self.friends.count()
    
    def watchers_count(self):
        return self.watchers.count()
    
    def posts_count(self):
        return self.post_set.count()

class Category(models.Model):
    NAME_MAX_LEN = 50
    DESCRIPTION_MAX_LEN = 1000
    name = models.CharField(max_length=NAME_MAX_LEN,unique=True)
    description = models.CharField(max_length=DESCRIPTION_MAX_LEN)
    picture = models.ImageField(upload_to='category_images')

    def delete(self):
        if self.picture:
            if os.path.isfile(self.picture.path):
                os.remove(self.picture.path)
        super().delete()

    def __str__(self):
        return self.name

class Post(models.Model):
    POST_MAX_LEN = 1000

    creator = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.CharField(max_length=POST_MAX_LEN)
    image = models.ImageField(upload_to='post_images', blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    roars = models.ManyToManyField(Account,related_name='roared_posts',blank=True)
    date = models.DateField(default=datetime.datetime(2025,1,1))

    def delete(self):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete()

    def __str__(self):
        return self.creator.__str__() + ":" + str(self.id)

class Comment(models.Model):
    COMMENT_MAX_LEN = 500

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    creator = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.CharField(max_length=COMMENT_MAX_LEN)
    date = models.DateTimeField(default=datetime.datetime(2025,1,1))

    def __str__(self):
        return self.post.__str__() + "-" + str(self.id) + f"({self.creator.__str__()})"