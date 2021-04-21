from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followee")

class Post(models.Model):
    post = models.CharField(max_length=280)
    
    post_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

class Likes(models.Model):
    liked_post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="liked_post")
    liked_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="liker")