__author__ = 'soroosh'

from django.conf.urls import patterns, url

from guarantor.views import *

urlpatterns = patterns('',
                       url(r'^(?i)register/(?P<request_id>\d*)', RegisterGuarantorView.as_view(),
                           name='register'),
)