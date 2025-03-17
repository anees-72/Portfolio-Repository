from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE


class User(AbstractUser):
    pass



class Posts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    content=models.TextField(max_length=350)
    likes=models.ManyToManyField(User,related_name="liked_posts",null=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    @property
    def likes_count(self):
        return self.likes.count()

class Follow(models.Model):
    follower=models.ForeignKey(User,on_delete=CASCADE,related_name="follower_name")
    following=models.ForeignKey(User,on_delete=CASCADE,related_name="following_name")
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower}: follows {self.following}"
