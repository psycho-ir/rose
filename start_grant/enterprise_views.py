from django.http import HttpResponse
from django.template import loader, RequestContext
from django.views.generic import View
from customer.models.enterprise_models import EnterpriseCustomerInformation, RegisterTown, BoadOfDirectorRole
from rose_config.models import CompanyType, Province, Town, JobCertificateType, LoanType, VasigheType, Bank
from start_grant.models import Request

__author__ = 'soroosh'


class EnterpriseSubmitDataView(View):
    def get(self, request, request_id):
        readonly = False
        if request.user.profile.role.name == 'superior':
            readonly = True
        customer_request = Request.objects.get(pk=request_id)
        if not customer_request.is_editable():
            readonly = True
        if customer_request.user_id != request.user.id:
            readonly = True

        customer_information = EnterpriseCustomerInformation.objects.filter(pk=customer_request.cif).first()
        company_types = CompanyType.objects.all()
        register_towns = RegisterTown.objects.all()
        provinces = Province.objects.all()
        towns = Town.objects.filter(province_id=provinces.first().id)
        certificate_types = JobCertificateType.objects.filter(type='hoghooghi',
                                                              business_part__id=customer_request.business_part_id)
        loan_types = LoanType.objects.all()
        refund_types = loan_types.first().refund_types.all()
        board_of_directors = BoadOfDirectorRole.objects.all()
        vasighe_types = VasigheType.objects.all()
        banks = Bank.objects.all()

        template = loader.get_template('enterprise_submit_data.html')
        context = RequestContext(request,
                                 {
                                     'readonly': readonly,
                                     'customer_info': customer_information,
                                     'customer_request': customer_request,
                                     'company_types': company_types,
                                     'register_towns': register_towns,
                                     'provinces': provinces,
                                     'towns': towns,
                                     'certificate_types': certificate_types,
                                     'loan_types': loan_types,
                                     'refund_types': refund_types,
                                     'board_of_directors': board_of_directors,
                                     'vasighe_types': vasighe_types, 'banks': banks})

        return HttpResponse(template.render(context))

        pass

    def post(self, request):
        pass