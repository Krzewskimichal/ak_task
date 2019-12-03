from django.urls import path
from task.views import MainSiteView, RegisterView, logout_view, login_view, PostView, CommentsView, ActivityService, \
    like_post_view, like_comment_view


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
    path('activityservice/', ActivityService.as_view(), name='activityservice'),
    # add like
    path('likepost/', like_post_view, name='likepost'),
    path('likecomment/', like_comment_view, name='likecomment'),
]
