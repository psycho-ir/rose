from django.conf.urls import patterns, include, url

from django.contrib import admin
from user_management.views import LoginView

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^(?i)dashboard/$', include('dashboard.urls', namespace='dashboard')),
                       url(r'^(?i)user/', include('user_management.urls', namespace='user')),
                       url(r'^(?i)grant/', include('start_grant.urls', namespace='grant')),
                       url(r'^(?i)core/', include('core_connection.urls', namespace='core')),
                       url(r'^(?i)customer/', include('customer.urls', namespace='customer')),
                       url(r'^(?i)config/', include('rose_config.urls', namespace='config')),
                       url(r'^(?i)guarantor/', include('guarantor.urls', namespace='guarantor')),
                       url(r'^(?i)superior/', include('superior.urls', namespace='superior')),
                       url(r'^(?i)notification/', include('notification.urls', namespace='notification')),
                       url(r'^$', LoginView.as_view()),
)


