from django.http import HttpResponse
from django.template import loader, RequestContext
from django.views.generic import View
from customer.models.enterprise_models import EnterpriseCustomerInformation, RegisterTown
from rose_config.models import CompanyType, Province, Town, JobCertificateType, LoanType
from start_grant.models import Request

__author__ = 'soroosh'


class EnterpriseSubmitDataView(View):
    def get(self, request, request_id):
        customer_request = Request.objects.get(pk=request_id)
        customer_information = EnterpriseCustomerInformation.objects.filter(pk=customer_request.cif).first()
        company_types = CompanyType.objects.all()
        register_towns = RegisterTown.objects.all()
        provinces = Province.objects.all()
        towns = Town.objects.filter(province_id=provinces.first().id)
        certificate_types = JobCertificateType.objects.all()
        loan_types = LoanType.objects.all()
        refund_types = loan_types.first().refund_types.all()

        template = loader.get_template('enterprise_submit_data.html')
        context = RequestContext(request,
                                 {'customer_info': customer_information,
                                  'customer_request': customer_request,
                                  'company_types': company_types,
                                  'register_towns': register_towns,
                                  'provinces': provinces,
                                  'towns': towns,
                                  'certificate_types': certificate_types,
                                  'loan_types': loan_types,
                                  'refund_types': refund_types})

        return HttpResponse(template.render(context))

        pass

    def post(self, request):
        pass