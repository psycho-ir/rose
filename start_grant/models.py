from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
import datetime
from core_connection import customer_repository, deposit_repository
from customer.models.common import CUSTOMER_TYPE, Customer
from customer.models.real_models import RealCustomerInformation
from guarantor.models import Guarantor
from rose_config.exceptions import ValidationException
from rose_config.models import BusinessPart, RequestDescription, LoanType, RefundType, Bank, VasigheType, config

REQUEST_STATUS = (
    ("intro", "intro"),
    ("req_info_completed", "req_info_completed"),
    ("ready_for_checklist", "ready_for_checklist"),
    ("checklist_completed", "checklist_completed"),
    ("enquiry_assigned", "enquiry_assigned")
)


class Request(models.Model):
    class Meta:
        ordering = ['-id']

    type = models.CharField(choices=CUSTOMER_TYPE, max_length=30)
    cif = models.CharField(max_length=20)
    deposit_number = models.CharField(max_length=20)
    register_date = models.DateTimeField(default=datetime.datetime.now)
    last_update = models.DateTimeField(default=datetime.datetime.now)
    user = models.ForeignKey(to=User, related_name='registered_requests')
    branch_code = models.IntegerField()
    business_part = models.ForeignKey(BusinessPart)
    request_description = models.ForeignKey(RequestDescription)
    has_loan_from_current_bank = models.BooleanField(default=True)
    request_amount = models.BigIntegerField(default=1000000)
    status = models.CharField(max_length=50, choices=REQUEST_STATUS, default='intro')
    guarantors = models.ManyToManyField(to=Guarantor, related_name='guaranted_requests')
    agent = models.ForeignKey(RealCustomerInformation, related_name='agent_requests', blank=True, null=True)

    def need_guarantor(self):
        if self.vasighe_information.vasighe_types.filter(Q(name='safte') | Q(name='cheque')).exists():
            return True
        else:
            return False


    def is_all_information_completed(self):
        if not hasattr(self, 'vasighe_information') or not hasattr(self, 'complete_information'):
            return False
        customer = Customer.objects.get(customer_code=self.cif)
        if customer.type == 'haghighi':
            if hasattr(customer, 'realcustomerinformation'):
                cus_info = customer.realcustomerinformation
                if hasattr(cus_info, 'contact_info') and hasattr(cus_info, 'job_info') and hasattr(cus_info,
                                                                                                   'asset_info') and hasattr(
                        cus_info, 'bank_income_info'):
                    return True
                else:
                    return False
            else:
                return False
        elif customer.type == 'hoghooghi':
            if customer.enterprisecustomerinformation is not None:
                cus_info = customer.enterprisecustomerinformation
                if cus_info.director_set.count() > 0 and hasattr(cus_info, 'contact_info') and hasattr(cus_info,
                                                                                                       'activity_info') and hasattr(
                        cus_info, 'asset_info') and cus_info.activity_info.count() > 0:
                    return True
                else:
                    return False
            else:
                return False
        else:
            raise Exception("customer type is not ok, it is: " + customer.type)

    def is_editable(self):
        if self.status == 'checklist_completed':
            return False
        return True

    @staticmethod
    def from_dic(dic, user):
        haghighi_max_loan_amount = config.objects.get(pk='HAGHIGHI_MAX_LOAN_AMOUNT')
        hoghooghi_max_loan_amount = config.objects.get(pk='HOGHOOGHI_MAX_LOAN_AMOUNT')
        customer = customer_repository.find_customer(dic['cif'])
        if len(customer) == 0:
            raise ValidationException("Customer does not exist")

        deposit = deposit_repository.find_deposit(dic['cif'], dic['deposit_number'])
        if len(deposit) == 0:
            raise ValidationException("Deposit and customer are not compatible")

        amount = int(dic['request_amount'])
        print amount
        if dic['type'] == 'haghighi':
            if amount > int(haghighi_max_loan_amount.value):
                raise ValidationException("Request amount is more than max")

        if dic['type'] == 'hoghooghi':
            if amount > int(hoghooghi_max_loan_amount.value):
                raise ValidationException("Request amount is more than max")

        if customer[0]["F51"] == '0' and dic['type'] == 'hoghooghi':
            raise ValidationException("Customer is enterprise but request is real")

        if customer[0]["F51"] == '1' and dic['type'] == 'haghighi':
            raise ValidationException("Customer is real but request is enterprise")

        request = Request(type=dic['type'], cif=dic['cif'], deposit_number=dic['deposit_number'], user_id=user.id,
                          branch_code=user.profile.branch_code,
                          business_part_id=dic['business_part'], request_description_id=dic['request_description'],
                          has_loan_from_current_bank=dic['has_loan_from_current_bank'] == 'True',
                          request_amount=dic['request_amount'])

        if dic.get('agent_national_number', None):
            request.agent_id = dic['agent_national_number']

        return request


class SanadMelkiInformation(models.Model):
    sanad_no = models.CharField(max_length=30)
    owner_name = models.CharField(max_length=60)
    current_value = models.BigIntegerField()
    address = models.CharField(max_length=500)

    @staticmethod
    def from_dic(dic):
        sanad = SanadMelkiInformation(sanad_no=dic['sanad_no'],
                                      owner_name=dic['owner_name'],
                                      current_value=dic['current_value'],
                                      address=dic['address']
        )

        return sanad


class RequestCompleteInformation(models.Model):
    request = models.OneToOneField(to=Request, related_name='complete_information', primary_key=True)
    prepayed_amount = models.BigIntegerField(default=0)
    loan_type = models.ForeignKey(LoanType)
    refund_duration = models.IntegerField(default=12)
    refund_period_type = models.CharField(default='month', max_length='20')
    refund_type = models.ForeignKey(RefundType)
    number_of_installments = models.IntegerField(default=12)

    @staticmethod
    def from_dic(dic):
        request = Request.objects.get(id=dic['request_id'])
        number_of_installments = int(dic['number_of_installments'])
        if request.request_amount < int(dic['prepayed_amount']):
            raise ValidationException("Prepayed amount cannot be more than request amount")
        refund_period_type = dic['refund_period_type']

        if refund_period_type != 'month' and refund_period_type != 'day':
            raise ValidationException("Refund period type can be month or day")

        if refund_period_type == 'day':
            if number_of_installments > 4:
                raise ValidationException("Number of installments cannot be more than 4 for daily")

        rci = RequestCompleteInformation(request_id=dic['request_id'], prepayed_amount=dic['prepayed_amount'],
                                         loan_type_id=dic['loan_type_id'], refund_duration=dic['refund_duration'],
                                         refund_type_id=dic['refund_type_id'],
                                         number_of_installments=number_of_installments,
                                         refund_period_type=dic['refund_period_type'])
        return rci

    def save(self, *args, **kwargs):
        super(RequestCompleteInformation, self).save(*args, **kwargs)
        self.request.status = 'req_info_completed'
        self.request.save()


class BankVasigheInformation(models.Model):
    request = models.OneToOneField(to=Request, related_name='vasighe_information', primary_key=True)
    banks = models.ManyToManyField(Bank, null=True, blank=True)
    vasighe_types = models.ManyToManyField(VasigheType, null=True, blank=True)
    sanad_melki_info = models.ForeignKey(SanadMelkiInformation, blank=True, null=True)

    @staticmethod
    def from_dic(dic, sanad):
        if sanad is None:
            bank_vasighe = BankVasigheInformation(request_id=dic['request_id'])

        else:
            bank_vasighe = BankVasigheInformation(request_id=dic['request_id'], sanad_melki_info_id=sanad.id)

        bank_vasighe.save()
        bank_vasighe.vasighe_types.clear()
        bank_vasighe.banks.clear()
        bank_vasighe.vasighe_types = dic.getlist('vasighe_types')
        bank_vasighe.banks = dic.getlist('banks')

        return bank_vasighe


class CheckListItem(models.Model):
    name = models.CharField(max_length=100)
    local_name = models.CharField(max_length=1000)
    description = models.CharField(max_length=2000)


class CheckList(models.Model):
    request = models.OneToOneField(Request, related_name='check_list', primary_key=True)

    def is_done(self):
        for item in self.items.all():
            if not item.checked:
                return False
        return True


class CheckListItemInstance(models.Model):
    item = models.ForeignKey(CheckListItem)
    checked = models.BooleanField(default=False)
    checklist = models.ForeignKey(CheckList, related_name='items')










