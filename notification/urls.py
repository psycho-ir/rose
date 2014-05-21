from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from notification.views import *


urlpatterns = patterns('',
                       url(r'^(?i)list', login_required(NotificationView.as_view(), login_url='/'), name='list'),


)