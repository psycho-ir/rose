"""
WSGI config for rose project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rose.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# import datetime
#
# from django_scheduler.simple_scheduler import ProcessSimpleScheduler
# from assign.models import *
#
#
# def say_hello():
#     print 'Number of enquiry assigns: %s' % EnquiryAssign.objects.count()
#
#
# scheduler = ProcessSimpleScheduler(5, say_hello)
# scheduler.run()