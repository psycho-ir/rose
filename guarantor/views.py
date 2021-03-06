from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.context import RequestContext
from django.views.generic import View
from customer.models import *
from customer.models import RealCustomerInformation, Customer
from guarantor.models import Guarantor
from rose_config.models import Province, Town, JobType, JobCertificateType
from start_grant.models import Request
from core_connection.customer_repository import *
import checker


class RegisterGuarantorView(View):
    def get(self, request, request_id):
        customer_id = request.GET.get('customer_id')
        customer_request = Request.objects.get(id=request_id)

        guarantor = None
        message = None
        context = None

        if customer_id is not None and customer_id != '':
            try:
                if len(find_customer(customer_id)) == 0:
                    message = 'customer does not exist'
                else:
                    guarantor = RealCustomerInformation.objects.get(customer_code=customer_id)
                    checker.check_guarantor(customer_request, guarantor)
                    # if customer_request.cif == customer_id:
                    # message = 'guarantor and request owner cannot be the same'
                    # customer = RealCustomerInformation.objects.get(pk=customer_id)

            except ObjectDoesNotExist as e:
                print e
            except checker.NotPermittedGuarantor as e:
                message = e.message

        template = loader.get_template("register_guarantor.html")
        if message is not None:
            context = RequestContext(request, {
                'customer_type': 'haghighi',
                'customer_request': customer_request,
                'message': message})

            return HttpResponse(template.render(context))

        provinces = Province.objects.all()
        towns = Town.objects.filter(province_id=provinces.first().id)
        all_towns = Town.objects.all()
        job_types = JobType.objects.all()
        certificate_types = JobCertificateType.objects.all()
        context = RequestContext(request, {'customer_type': 'haghighi', 'customer_request': customer_request,
                                           'customer': guarantor,
                                           'provinces': provinces,
                                           'towns': towns,
                                           'all_towns': all_towns,
                                           'job_types': job_types,
                                           'certificate_types': certificate_types,
                                           'customer_id': customer_id,
                                           'message': message
        })

        return HttpResponse(template.render(context))

    def post(self, request, request_id):
        customer_request = Request.objects.get(pk=request_id)
        if customer_request.cif == request.POST.get('customer_id'):
            raise Exception('guarantor and request owner cannot be the same')
        guarantor = Guarantor()
        guarantor.customer_id = request.POST.get('customer_id')
        guarantor.vasighe_type_id = 1

        if customer_request.guarantors.filter(customer_id=guarantor.customer_id).exists():
            return HttpResponseRedirect(reverse('guarantor:register', args=[request_id]))

        guarantor.save()
        customer_request.guarantors.add(guarantor)

        return HttpResponseRedirect(reverse('guarantor:list', args=[request_id]))


class GuarantorListView(View):
    def get(self, request, request_id):
        readonly = False
        if request.user.profile.role.name == 'superior':
            readonly = True
        customer_request = Request.objects.get(pk=request_id)

        if customer_request.user_id != request.user.id:
            readonly = True

        if customer_request.need_guarantor():
            context = RequestContext(request, {
                'readonly': readonly,
                'guarantors': customer_request.guarantors.all(),
                'request_id': request_id})
        else:
            context = RequestContext(request,
                                     {'message': 'This request does not need guarantor', 'request_id': request_id})

        template = loader.get_template('guarantor_list.html')
        return HttpResponse(template.render(context))


class GuarantorRemoveView(View):
    def post(self, request, request_id, guarantor_id):
        r = Request.objects.get(pk=request_id)
        r.guarantors.remove(guarantor_id)
        return HttpResponseRedirect(reverse('guarantor:list', args=[request_id]))

