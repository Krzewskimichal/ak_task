from task.models import UserModel, PostModel, CommentModel, LikesModel, Active
from django.shortcuts import render, redirect
from datetime import datetime
from math import ceil
from django.contrib.auth.models import User


class ActivityService:

    @staticmethod
    def active(*args, **kwargs):
        """
        get logged user
        return two list, group and single,
        group: contains grouped activities
        single: contains single activities
        """
        user = kwargs['user']
        subscribers = UserModel.objects.filter(user=user)
        #  get all subscribed users
        sub = []
        for i in subscribers:
            sub.append(User.objects.filter(username=i.user_subscribe))

        #  get all Activities of subscribe users
        all_subscribers = []
        for subscriber in sub:
            for i in subscriber:
                    all_subscribers.append(Active.objects.filter(user=i).order_by('-date'))

        one_queryset = []
        #  count time for subscribers
        for i in all_subscribers:
            for z in i:
                z.date = time_count(z.date)
                one_queryset.append(z)

        actives = Active.objects.filter(user=user).order_by('-date')
        all_activities = []

        for active in actives:
            active.date = time_count(active.date)
            all_activities.append(active)

        all_activities += one_queryset
        #  container for group elements
        group = []
        #  container for single elements
        single = []

        #  check if activities are in the same group
        for active in all_activities:
            for z in all_activities:
                if active.date[0] == z.date[0] and active.date[1] == z.date[1] and active.object_id != z.object_id and \
                        active.activity_type == z.activity_type and active.user == z.user and active not in group:
                    group.append(active)

        #  add activity to single list
        for active in all_activities:
            if active not in group:
                single.append(active)

        return group, single


def time_count(date):
    """
    get date and return time in seconds
    """
    now = datetime.now().timestamp()
    published = date.timestamp()
    time = now - published

    if time < 3600:  # minutes
        time /= 60
        time = ceil(time)
        time_mark = 'minutes'
    elif 3600 <= time < 86400:  # houres
        time /= 3600
        time = ceil(time)
        time_mark = 'hours'
    elif 86400 <= time < 604800:  # days
        time /= 86400
        time = ceil(time)
        time_mark = 'days'
    elif 604800 <= time < 2630000:  # weeks
        time /= 604800
        time = ceil(time)
        time_mark = 'weeks'
    elif 2630000 <= time < 31536000:  # months
        time /= 2630000
        time = ceil(time)
        time_mark = 'months'
    else:  # years
        time /= 31536000
        time = ceil(time)
        time_mark = 'years'
    return time, time_mark
