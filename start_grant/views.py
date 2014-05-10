from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.views.generic import View
from start_grant.models import Request

__author__ = 'soroosh'

from rose_config.models import config, JobType, JobCertificateType, Province, Town, LoanType, RefundType, Bank, \
    VasigheType, BusinessPlace, BusinessPart, RequestDescription


class StartView(View):
    def get(self, request):
        haghighi_max_loan_amount = config.objects.get(pk='HAGHIGHI_MAX_LOAN_AMOUNT')
        hoghooghi_max_loan_amount = config.objects.get(pk='HOGHOOGHI_MAX_LOAN_AMOUNT')
        business_parts = BusinessPart.objects.all()
        request_descriptions = RequestDescription.objects.filter(business_parts=business_parts.first().id)

        template = loader.get_template("start.html")
        context = RequestContext(request,
                                 {
                                     'business_parts': business_parts, 'request_descriptions': request_descriptions,
                                     'haghighi_max_loan_amount': haghighi_max_loan_amount,
                                     'hoghooghi_max_loan_amount':
                                         hoghooghi_max_loan_amount})
        return HttpResponse(template.render(context))

    def post(self, request):
        haghighi_max_loan_amount = config.objects.get(pk='HAGHIGHI_MAX_LOAN_AMOUNT')
        hoghooghi_max_loan_amount = config.objects.get(pk='HOGHOOGHI_MAX_LOAN_AMOUNT')

        request = Request.from_dic(request.POST, request.user)
        request.save()

        if request.type == 'haghighi':
            return HttpResponseRedirect(reverse('grant:submit', args=(request.id,)))

        if request.type == 'hoghooghi':
            return HttpResponseRedirect(reverse('grant:enterprise_submit', args=(request.id,)))

        return HttpResponse("Fatal Error %s" % request.type)