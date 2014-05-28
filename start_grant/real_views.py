from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.context import RequestContext
from django.views.generic import View
from customer.models.real_models import RealCustomerInformation
from rose_config.models import JobType, JobCertificateType, Province, Town, LoanType, RefundType, Bank, \
    VasigheType, BusinessPlace
from start_grant.checklist import createCheckList
from start_grant.models import Request, RequestDescription, RequestCompleteInformation
from django.core import serializers


class SubmitDataView(View):
    def get(self, request, request_id):
        readonly = False
        if request.user.profile.role.name == 'superior':
            readonly = True
        customer_request = Request.objects.get(id=request_id)
        if customer_request.user_id != request.user.id:
            readonly = True
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
                                 {
                                     'readonly': readonly,
                                     'customer_info': customer_information,
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

        if not customer_request.is_all_information_completed():
            return HttpResponseRedirect(reverse('grant:submit', args=[request_id]))

        createCheckList(customer_request)

        customer_request.status = 'ready_for_checklist'
        customer_request.save()

        if customer_request.need_guarantor():
            return HttpResponseRedirect(reverse('guarantor:list', args=[request_id]))

        else:
            return HttpResponseRedirect(reverse('grant:track'))


class ReqCompleteView(View):
    def post(self, request):
        try:
            complete_info = RequestCompleteInformation.from_dic(request.POST)
            complete_info.save()
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

