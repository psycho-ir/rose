from django.http import HttpResponse
from django.template import loader, RequestContext
from django.views.generic import View
from customer.models.enterprise_models import EnterpriseCustomerInformation
from start_grant.models import Request

__author__ = 'soroosh'


class EnterpriseSubmitDataView(View):
    def get(self, request,request_id):
        customer_request = Request.objects.get(pk='request_id')
        customer_information = EnterpriseCustomerInformation.objects.filter(pk=customer_request.cif).first()

        template = loader.get_template('enterprise_submit_data.html')
        context = RequestContext(request,
                                 {'customer_info': customer_information,
                                  'customer_request': customer_request})

        return HttpResponse(template.render(context))

        pass

    def post(self, request):
        pass