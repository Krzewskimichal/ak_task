from django.contrib.auth.models import User
from task.forms import LoginForm


def my_cp(request):
    if request.user.is_authenticated:
        logged = True
        username = request.user.username
    else:
        username = ''
        logged = False

    login_form = LoginForm()
    data = {
        'login_form': login_form,
        'logged': logged,
        'username': username,
    }
    return data
