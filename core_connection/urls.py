from django.conf.urls import patterns, url

from core_connection.views import *

urlpatterns = patterns('',
                       url(r'^(?i)check_custor/(?P<customer_id>\d*)', is_customer_valid, name='is_customer_valid'),
                       url(
                           r'^(?i)check_deposit/(?P<customer_id>\d*)-(?P<deposit_number_1>\d*)-(?P<deposit_number_2>\d*)', is_deposit_valid, name='is_deposit_valid')
)