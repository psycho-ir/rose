import json
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.context import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import View
from customer.models.real_models import RealCustomerInformation
from rose_config.models import config, JobType, JobCertificateType, Province, Town, LoanType, RefundType, Bank, \
    VasigheType, BusinessPlace
from start_grant.models import Request, BusinessPart, RequestDescription, RequestCompleteInformation


class SubmitDataView(View):
    def get(self, request, request_id):
        customer_request = Request.objects.get(id=request_id)
        customer_information = RealCustomerInformation.objects.filter(pk=customer_request.cif).first()
        job_types = JobType.objects.all()
        certificate_types = JobCertificateType.objects.all()
        provinces = Province.objects.all()
        towns = Town.objects.filter(province_id=provinces.first().id)
        loan_types = LoanType.objects.all()
        refund_types = loan_types.first().refund_types.all()
        banks = Bank.objects.all()
        business_places = BusinessPlace.objects.all()
        vasighe_types = VasigheType.objects.all()
        template = loader.get_template('submit_data.html')
        context = RequestContext(request,
                                 {'customer_info': customer_information,
                                  'customer_request': customer_request,
                                  'provinces': provinces,
                                  'towns': towns,
                                  'job_types': job_types,
                                  'certificate_types': certificate_types,
                                  'loan_types': loan_types,
                                  'refund_types': refund_types,
                                  'banks': banks,
                                  'vasighe_types': vasighe_types,
                                  'business_places': business_places})
        return HttpResponse(template.render(context))

    def post(self, request, request_id):
        customer_request = Request.objects.get(id=request_id)

        if Request.objects.get(id=2).need_guarantor():
            return HttpResponseRedirect(reverse('guarantor:list', args=[request_id]))

        else:
            return HttpResponseRedirect(reverse('grant:track'))



from django.core import serializers


class ReqCompleteView(View):
    def post(self, request):
        try:
            complete_info = RequestCompleteInformation.from_dic(request.POST)
            complete_info.save()
            # r = Request.objects.get(pk=request.POST.get('request_id'))
            # r.status = 'req_info_completed'
            # r.save()
            return HttpResponse("True")
        except Exception as e:
            print e
            return HttpResponse("False")


class RequestDescriptionsView(View):
    def get(self, request):
        if request.GET["business_part"] is not None:
            request_descriptions = RequestDescription.objects.filter(business_parts=request.GET["business_part"])
            encoded = serializers.serialize('json', request_descriptions)
            return HttpResponse(encoded)

