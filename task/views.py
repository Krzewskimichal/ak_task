from django.shortcuts import render, redirect
from django.views import View
from task.forms import RegisterForm, LoginForm, PostForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from task.models import PostModel, UserModel, CommentModel
from datetime import datetime


class MainSiteView(View):
    """
    main site
    """
    def get(self, request):
        posts = PostModel.objects.all().order_by('published')
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
                usermodel = UserModel(user=request.user)
                usermodel.save()
                return redirect('/')


def login_view(request):
    """
    user login
    :param request:
    :return: redirect to main site
    """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    login(request, user)
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
        form = AddPostForm()
        data = {
            'add_post_form': form,
        }
        return render(request, 'add_post.html', data)

    def post(self, request):
        data = PostForm(request.POST)
        if data.is_valid():
            title = data.cleaned_data['title']
            content = data.cleaned_data['content']
            post = PostModel(author=request.user, title=title, content=content)
            post.save()
            return redirect('/')


class CommentsView(View):
    """
    View allow add and show comments of posts
    """
    def get(self, request):
        post_id = request.GET['post_id']
        post = PostModel.objects.get(id=post_id)
        comments = CommentModel.objects.filter(target_post=post.id)
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
        return redirect('/')


def time_count(date):
    now = datetime.now().timestamp()
    publicshed = date.timestamp()
    time = now - publicshed
    return time


class ActivityService(View):

    def get(self, request):
        get_method = True
        users = User.objects.all()
        data = {
            'users': users,
            'get_method': get_method,
        }
        return render(request, 'activityservice.html', data)

    def post(self, request):
        user = request.POST['user']
        user = User.objects.get(username=user)
        posts = PostModel.objects.filter(author=user).order_by('published')
        comments = CommentModel.objects.filter(author=user).order_by('published')
        data = {
            'user': user,
            'comments': comments,
            'posts': posts,
        }
        return render(request, 'activityservice.html', data)
