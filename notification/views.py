from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import loader, RequestContext
from django.views.generic import View
from superior.models import Assign


class NotificationView(View):
    def get(self, request):
        assigns = Assign.objects.filter(target__id=request.user.id)

        template = loader.get_template('notification_list.html')
        context = RequestContext(request, {'assigns': assigns})

        return HttpResponse(template.render(context))
