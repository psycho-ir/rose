from functools import wraps
from django.http import HttpResponseRedirect
from rose import settings


def is_user_anon(login_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view, *args, **kwargs):
            if view.request.user.is_authenticated():
                return HttpResponseRedirect(settings.DEFAULT_LOGIN_URL)
            else:
                return view_func(view,view.request, *args, **kwargs)

        return _wrapped_view

    return decorator