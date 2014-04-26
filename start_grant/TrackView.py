from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.template.context import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import View
from start_grant.models import Request

__author__ = 'soroosh'


class TrackView(View):

    def get(self, request):
        template = loader.get_template('track.html')
        requests = Request.objects.filter(branch_code=request.user.profile.branch_code)
        context = RequestContext(request, {'requests': requests})
        return HttpResponse(template.render(context))