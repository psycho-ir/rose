from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
import datetime
from customer.models.common import CUSTOMER_TYPE
from guarantor.models import Guarantor
from rose_config.models import BusinessPart, RequestDescription, LoanType, RefundType, Bank, VasigheType


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
    status = models.CharField(max_length=50, default='intro')
    guarantors = models.ManyToManyField(to=Guarantor, related_name='guaranted_requests')

    def need_guarantor(self):
        if self.vasighe_information.vasighe_types.filter(Q(id=2) | Q(id=3)).exists():
            return True
        else:
            return False

    @staticmethod
    def from_dic(dic, user):
        request = Request(type=dic['type'], cif=dic['cif'], deposit_number=dic['deposit_number'], user_id=user.id,
                          branch_code=user.profile.branch_code,
                          business_part_id=dic['business_part'], request_description_id=dic['request_description'],
                          has_loan_from_current_bank=dic['has_loan_from_current_bank'] == 'True',
                          request_amount=dic['request_amount'])

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
    refund_type = models.ForeignKey(RefundType)
    number_of_installments = models.IntegerField(default=12)

    @staticmethod
    def from_dic(dic):
        rci = RequestCompleteInformation(request_id=dic['request_id'], prepayed_amount=dic['prepayed_amount'],
                                         loan_type_id=dic['loan_type_id'], refund_duration=dic['refund_duration'],
                                         refund_type_id=dic['refund_type_id'],
                                         number_of_installments=dic['number_of_installments'])
        return rci


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








