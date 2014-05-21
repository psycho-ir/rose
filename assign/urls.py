__author__ = 'soroosh'

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from assign.views import *


urlpatterns = patterns('',
                       url(r'^(?i)tasks', login_required(TaskListView.as_view(), login_url='/'), name='tasks'),
                       url(r'^(?i)enquiry_assign/(?P<request_id>\d*)', login_required(EnquiryAssignView.as_view(), login_url='/'),
                           name='enquiry_assign')

)

