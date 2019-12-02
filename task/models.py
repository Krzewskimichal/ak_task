from django.db import models
from django.contrib.auth.models import User


# additional content for users
class UserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_subscribe = models.IntegerField(default=0)


class PostModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(blank=False, max_length=256)
    content = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    like = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class CommentModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=False, max_length=1024)
    published = models.DateTimeField(auto_now=True)
    target_post = models.ForeignKey(PostModel, on_delete=models.CASCADE)


class UsersActivityModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # if user add post, target_user can be blank
    target_user = models.ForeignKey(User, related_name='target_user', on_delete=models.CASCADE, blank=True, null=True)
    activity_choices = [
        ('subscribe', 'subscribe'),
        ('post', 'post'),
        ('comment', 'comment'),
        ('like', 'like'),
    ]
    activity = models.CharField(max_length=32, choices=activity_choices, default='post', blank=False)
