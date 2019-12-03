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
    like = models.IntegerField(default=0)


class PostsLikesModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)


class CommentsLikesModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
