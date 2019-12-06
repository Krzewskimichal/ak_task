from django.shortcuts import render, redirect
from django.views import View
from task.forms import RegisterForm, LoginForm, PostForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from task.models import PostModel, UserModel, CommentModel, LikesModel, Active
from django.contrib import messages
from task.services import time_count, ActivityService


class MainSiteView(View):
    """
    main site
    """
    def get(self, request):
        posts = PostModel.objects.all().order_by('-published')
        for post in posts:
            post.published = time_count(post.published)

        data = {
            'posts': posts,
        }
        return render(request, 'mainsite.html', data)


class RegisterView(View):
    """
    register new user
    """

    def get(self, request):
        register_form = RegisterForm()
        form = {
            'form': register_form,
        }
        return render(request, 'register.html', form)

    def post(self, request):
        data = RegisterForm(request.POST)
        if data.is_valid():
            username = data.cleaned_data['username']
            password1 = data.cleaned_data['password1']
            password2 = data.cleaned_data['password2']
            email = data.cleaned_data['email']
            if password1 != password2:
                pass
            else:
                User.objects.create_user(username=username, password=password1, email=email)
                user = authenticate(username=username, password=password1)
                login(request, user)

                return redirect('/')


def login_view(request):
    """
    user login
    :param request:
    :return: redirect to main site
    """
    username = request.POST['username']
    password = request.POST['password']
    if authenticate(username=username, password=password):
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')
    else:
        messages.error(request, 'Incorrect login or password.')
        return redirect('/')


def logout_view(request):
    """
    user logout
    :param request:
    :return: redirect to main site
    """
    logout(request)
    return redirect('/')


class PostView(View):
    """
    View display all posts
    """
    def get(self, request):
        form = PostForm()
        data = {
            'add_post_form': form,
        }
        return render(request, 'add_post.html', data)

    """
    add new posts
    """
    def post(self, request):
        data = PostForm(request.POST)
        if data.is_valid():
            title = data.cleaned_data['title']
            content = data.cleaned_data['content']
            post = PostModel(author=request.user, title=title, content=content)
            post.save()

            active = Active(user=request.user, activity_type='p', content_object=post)
            active.save()
            return redirect('/')


class CommentsView(View):
    """
    View allow add and show comments of posts
    """
    def get(self, request):
        post_id = request.GET['post_id']
        post = PostModel.objects.get(id=post_id)
        post.published = time_count(post.published)
        comments = CommentModel.objects.filter(target_post=post.id)
        for coment in comments:
            coment.published = time_count(coment.published)
        data = {
            'post': post,
            'comments': comments,
        }
        return render(request, 'comment.html', data)

    def post(self, request):
        content = request.POST['content']
        post_id = request.POST['post_id']
        target_post = PostModel.objects.get(id=post_id)
        author = request.user
        comment = CommentModel(author=author, content=content, target_post=target_post)
        comment.save()

        active = Active(user=request.user, activity_type='c', content_object=comment)
        active.save()
        return redirect('/')


class NotificationsView(View):
    """
    when get method, selsect user, then choice activity
    """
    def get(self, request):
        user = request.user
        actives = ActivityService.active(user=user)
        data = {
            'group': actives[0],
            'single': actives[1],
        }
        return render(request, 'notifications.html', data)


def like_view(request):
    """
    get post_id and add like to database
    """
    #  check if user is logged
    # if request.user.is_authenticated:
    #     user = request.user
    #     comment = ''
    #     post = ''
    #
    #     #  check what user liked
    #     if 'comment' in request.GET:
    #         comment = request.GET['comment']
    #         obj = CommentModel.objects.get(id=comment)
    #     else:
    #         post = request.GET['post']
    #         obj = PostModel.objects.get(id=post)
    #
    #     #  check if user liked earlier
    #     if Active.objects.filter(user=user, content_object=obj):
    #         messages.error(request, 'Your already liked this post.')
    #         return redirect('/')
    #     else:
    #         # add like to CommentModel or LikeModel
    #         if comment != '':
    #             comment = CommentModel.objects.get(id=comment)
    #             comment.like += 1
    #             comment.save()
    #         else:
    #             post = PostModel.objects.ge(id=post)
    #             post.like += 1
    #             post.save()
    #
    #         active = Active(user=request.user, activity_type='l', content_object=obj)
    #         active.save()
    #     return redirect('/')
    # else:
    #     messages.error(request, 'You have to be logged..')
    #     return redirect('/')


def subscribe_view(request):
    """
    add subscriptions
    """
    user = request.user
    author_id = request.POST['author_id']
    target_user = User.objects.get(id=author_id)
    #  check if user subscribe user earlier
    if UserModel.objects.filter(user=user, user_subscribe=target_user):
        messages.error('You already subscribe this user.')
        return redirect('/')
    #  check if user try subscribe himself
    elif UserModel.objects.filter(user=user, user_subscribe=user):
        messages.error('You cant subscribe your self.')
        return redirect('/')
    else:
        user_model = UserModel(user=user, user_subscribe=target_user)
        user_model.save()

        active = Active(user=user, activity_type='s', content_object=user_model)
        active.save()
        return redirect('/')
