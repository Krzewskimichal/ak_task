from django.urls import path
from task.views import MainSiteView, RegisterView, logout_view, login_view, PostView, CommentsView, NotificationsView, \
    like_view, subscribe_view


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
    path('notifications/', NotificationsView.as_view(), name='notifications'),
    # add like
    path('like/', like_view, name='like'),
    # add subscriptions
    path('subscribe', subscribe_view, name='subscribe'),
]
