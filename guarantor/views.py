from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.context import RequestContext
from django.views.generic import View
from customer.models import RealCustomerInformation
from guarantor.models import Guarantor
from rose_config.models import Province, Town, JobType, JobCertificateType
from start_grant.models import Request
from core_connection.customer_repository import *


class RegisterGuarantorView(View):
    def get(self, request, request_id):
        customer_id = request.GET.get('customer_id')
        customer = None
        message = None
        if customer_id is not None and customer_id != '':
            try:
                if len(find_customer(customer_id)) == 0:
                    message = 'customer does not exist'
                customer = RealCustomerInformation.objects.get(pk=customer_id)

            except ObjectDoesNotExist as e:
                print e

        provinces = Province.objects.all()
        towns = Town.objects.filter(province_id=provinces.first().id)
        customer_request = Request.objects.get(id=request_id)
        job_types = JobType.objects.all()
        certificate_types = JobCertificateType.objects.all()
        context = RequestContext(request, {'customer_type': 'haghighi', 'customer_request': customer_request,
                                           'customer': customer,
                                           'provinces': provinces,
                                           'towns': towns,
                                           'job_types': job_types,
                                           'certificate_types': certificate_types,
                                           'customer_id': customer_id,
                                           'message': message
        })
        template = loader.get_template("register_guarantor.html")

        return HttpResponse(template.render(context))

    def post(self, request, request_id):
        guarantor = Guarantor()
        guarantor.customer_id = request.POST.get('customer_id')
        guarantor.vasighe_type_id = 1

        request = Request.objects.get(pk=request_id)
        if request.guarantors.filter(customer_id=guarantor.customer_id).exists():
            return HttpResponseRedirect(reverse('guarantor:register', args=[request_id]))

        guarantor.save()
        request.guarantors.add(guarantor)

        return HttpResponseRedirect(reverse('guarantor:list', args=[request_id]))


class GuarantorListView(View):
    def get(self, request, request_id):
        customer_request = Request.objects.get(pk=request_id)

        context = RequestContext(request, {'guarantors': customer_request.guarantors.all(),
                                           'request_id': request_id})
        template = loader.get_template('guarantor_list.html')

        return HttpResponse(template.render(context))


class GuarantorRemoveView(View):
    def post(self, request, request_id, guarantor_id):
        r = Request.objects.get(pk=request_id)
        r.guarantors.remove(guarantor_id)
        return HttpResponseRedirect(reverse('guarantor:list', args=[request_id]))

