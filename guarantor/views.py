from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.template.context import RequestContext
from django.views.generic import View
from start_grant.models import Request


class RegisterGuarantorView(View):
    def get(self, request, request_id):
        customer_request = Request.objects.get(id=request_id)
        context = RequestContext(request, {'customer_request': customer_request})
        template = loader.get_template("register_guarantor.html")

        return HttpResponse(template.render(context))

