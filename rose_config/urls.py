from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from rose_config.views import *


urlpatterns = patterns('',
                       url(r'^(?i)town/province_id=(?P<province_id>\d*)',
                           login_required(TownView.as_view(), login_url='/'), name='town'),
                       url(r'^(?i)refund/loan_type_id=(?P<loan_type_id>\d*)',
                           login_required(RefundTypeView.as_view(), login_url='/'), name='refund_type'),
)