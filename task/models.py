from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


# user subscribtions
class UserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_subscribe = models.ForeignKey(User, related_name='user_subscribe', on_delete=models.CASCADE)

    def __str__(self):
        return self.user_target


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


class LikesModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #  todo |name Active is not defined| dlaczego?
    # object = GenericRelation(Active)


class Active(models.Model):
    activity = (
        ('p', 'post'),
        ('l', 'ike'),
        ('c', 'comment'),
        ('s', 'subscribe'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=1, choices=activity)
    date = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
