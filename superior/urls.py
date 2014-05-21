from superior.views import TaskListView

__author__ = 'soroosh'

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
                       url(r'^(?i)tasks', login_required(TaskListView.as_view(), login_url='/'), name='tasks'),
)

