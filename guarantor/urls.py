__author__ = 'soroosh'

from django.conf.urls import patterns, url

from guarantor.views import *

urlpatterns = patterns('',
                       url(r'^(?i)register/(?P<request_id>\d*)', RegisterGuarantorView.as_view(),
                           name='register'),

                       url(r'^(?i)list/(?P<request_id>\d*)', GuarantorListView.as_view(),
                           name='list'),
                       url(r'^(?i)remove/(?P<request_id>\d*)/(?P<guarantor_id>\d*)', GuarantorRemoveView.as_view(),
                           name='remove'),

)