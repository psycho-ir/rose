from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import loader, RequestContext
from django.views.generic import View


class DashboardView(View):
    def get(self, request):
        template = loader.get_template("test.html")
        context = RequestContext(request)
        return HttpResponse(template.render(context))

    def post(self, request):
        return HttpResponse("POST!")

