from django.urls import path
from task.views import MainSiteView, RegisterView, logout_view, login_view, PostView, CommentsView, ActivityService


urlpatterns = [
    path('', MainSiteView.as_view(), name='main_site'),
    path('register/', RegisterView.as_view(), name='register'),
    # login/out views
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # add post form
    path('addpost/', PostView.as_view(), name='addpost'),
    path('comments/', CommentsView.as_view(), name='comments'),
    # activityservice
    path('activityservice/', ActivityService.as_view(), name='activityservice')
]
