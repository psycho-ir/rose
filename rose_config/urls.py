from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from rose_config.views import *


urlpatterns = patterns('',
                       url(r'^(?i)town/province_id=(?P<province_id>\d*)',
                           login_required(TownView.as_view(), login_url='/'), name='town'),
)