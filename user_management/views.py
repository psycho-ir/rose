import logging
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader, RequestContext
from django.views.generic import View
from rose import settings
from user_management.login import auth_user
from user_management.utils import is_user_anon

errorLogger = logging.getLogger('error')


class LoginView(View):

    @is_user_anon(login_url=settings.DEFAULT_LOGIN_URL)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)


    def get(self, request):
        template = loader.get_template("login.html")
        context = RequestContext(request)
        return HttpResponse(template.render(context))

    def post(self, request):
        return auth_user(request)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.DEFAULT_LOGOUT_URL)
