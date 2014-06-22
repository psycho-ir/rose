from django.http import HttpResponse

__author__ = 'soroosh'

from django.utils.translation import ugettext as _

def generate_ok_response():
    return HttpResponse('{"status":true}')

def generate_error_response(error_msg=None):
    if error_msg is None:
        return HttpResponse('{"status":false}')
    else:
        return HttpResponse('{"status":false,"error_message":"%s"}' % _(error_msg))


