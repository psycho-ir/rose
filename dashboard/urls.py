from django.conf.urls import patterns, url
from dashboard.views import *


urlpatterns = patterns('',
                       url(r'^', DashboardView.as_view(), name='login'),
)