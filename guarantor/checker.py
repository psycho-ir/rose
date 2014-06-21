from customer.models import EnterpriseCustomerInformation, Customer
from customer.models.real_models import RealCustomerInformation

__author__ = 'soroosh'


def check_guarantor(request, customer):
    if customer.type == 'haghighi':
        RealGuarantorChecker(request, customer.customer_code).check()


class EnterpriseGuarantorChecker:
    def __init__(self, request, guarantor_id):
        self.request = request
        self.customer = RealCustomerInformation.objects.get(id=request.cif)
        self.guarantor_id = guarantor_id

    def check(self):
        pass


class RealGuarantorChecker:
    def __init__(self, request, guarantor_id):
        self.request = request
        ##self.customer = RealCustomerInformation.objects.get(id=request.cif)
        self.guarantor_id = guarantor_id

    def check(self):
        if self.request.type == 'hoghooghi':
            self._handle_enterprise_request()
        elif self.request.type == 'haghighi':
            self._handle_real_request()

        else:
            raise Exception("Request type is not OK. Request Type: %s" % self.request.type)


    def _handle_real_request(self):
        customer = RealCustomerInformation.objects.get(customer_code=self.request.cif)
        if customer.customer_code == self.guarantor_id:
            raise NotPermittedGuarantor("guarantor and request owner cannot be the same")


    def _handle_enterprise_request(self):
        customer = EnterpriseCustomerInformation.objects.get(customer_code=self.request.cif)
        for director in customer.director_set.all():
            if director.customer_id == self.guarantor_id:
                raise NotPermittedGuarantor("Guarantor should not be in directors of company")


class NotPermittedGuarantor(Exception):
    def __init__(self, msg):
        self.message = msg






