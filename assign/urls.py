__author__ = 'soroosh'

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from assign.views import *


urlpatterns = patterns('',
                       url(r'^(?i)enquiry_assign/(?P<request_id>\d*)',
                           login_required(EnquiryAssignView.as_view(), login_url='/'),
                           name='enquiry_assign'),
                       url(r'^(?i)enquiry_response/(?P<assign_id>\d*)',
                           login_required(EnquiryResponseView.as_view(), login_url='/'), name='enquiry_response'),
                       url(r'^(?i)enquiry_response_start',
                           login_required(EnquiryActionResponseStartView.as_view(), login_url='/'),
                           name='enquiry_response_start'),
                       url(r'^(?i)enquiry_response_stop',
                           login_required(EnquiryActionResponseStopView.as_view(), login_url='/'),
                           name='enquiry_response_stop'),
                       url(r'^(?i)enquiry_response_complete',
                           login_required(EnquiryActionResponseCompleteView.as_view(), login_url='/'),
                           name='enquiry_response_complete'),
)

