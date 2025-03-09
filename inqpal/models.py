from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    fav_dino = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    def __str__(self):
        return self.user.username

class Post(models.Model):
    POST_MAX_LEN = 2000

    creator = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.CharField(max_length=POST_MAX_LEN)
    image = models.ImageField(upload_to='post_images', blank=True)
    category = models.CharField(max_length=50)
    roars = models.ManyToManyField(Account,related_name='roared_posts')

    def __str__(self):
        return self.creator.__str__() + ":" + str(self.id)

class Comment(models.Model):
    COMMENT_MAX_LEN = 500

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    creator = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.CharField(max_length=COMMENT_MAX_LEN)

    def __str__(self):
        return self.post.__str__() + "-" + str(self.id) + f"({self.creator.__str__()})"