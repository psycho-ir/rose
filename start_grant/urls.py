from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from start_grant import TrackView
from start_grant.views import *
from start_grant.enterprise_views import EnterpriseSubmitDataView
from start_grant.real_views import RequestDescriptionsView, SubmitDataView, ReqCompleteView


urlpatterns = patterns('',
                       url(r'^(?i)start$', login_required(StartView.as_view(), login_url='/'), name='start'),
                       url(r'^(?i)request_description',
                           login_required(RequestDescriptionsView.as_view(), login_url='/'),
                           name='request_description'),
                       url(r'^(?i)track', login_required(TrackView.TrackView.as_view(), login_url='/'), name='track'),
                       url(r'^(?i)submit/request_id=(?P<request_id>\d*)',
                           login_required(SubmitDataView.as_view(), login_url='/'), name='submit'),
                       url(r'^(?i)complete_request', login_required(ReqCompleteView.as_view(), login_url='/'),
                           name='complete_request'),
                       url(r'^(?i)enterprise_submit/request_id=(?P<request_id>\d*)',
                           login_required(EnterpriseSubmitDataView.as_view(), login_url='/'), name='enterprise_submit'),
                       url(r'^(?i)check_list/(?P<request_id>\d*)',
                           login_required(CheckListView.as_view(), login_url='/'), name='check_list')

)