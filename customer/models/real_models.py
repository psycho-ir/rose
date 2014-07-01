from customer.models.common import Customer
from rose_config.exceptions import ValidationException

__author__ = 'soroosh'

from django.db import models
from jdatetime import datetime as jalali_datetime
from rose_config.models import Town, Province, JobType, JobCertificateType, Bank, VasigheType, BusinessPlace
from datetime import datetime, timedelta


class RealCustomerInformation(Customer):
    class Meta:
        app_label = 'customer'

    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    bc_number = models.CharField(max_length=20)
    bc_serial_number = models.CharField(max_length=20)
    birth_date = models.DateTimeField()
    bc_place = models.ForeignKey(Town, related_name='customer_bc_places', null=True, blank=True)
    birth_place = models.ForeignKey(Town, related_name='customer_birth_places', null=True, blank=True)
    gender = models.CharField(max_length=10)

    def get_persian_birth_date(self):
        return jalali_datetime.fromgregorian(datetime=self.birth_date).strftime('%Y/%m/%d')

    def is_information_completed(self):
        if hasattr(self, 'contact_info') and hasattr(self, 'asset_info') and hasattr(self, 'bank_income_info'):
            return True
        return False

    @staticmethod
    def from_dic(dic):
        from utils.date_utils import greg_date_from_shamsi

        gregorian_birth_date = greg_date_from_shamsi(dic['birth_date'], '/')
        # timedelta(days=365*18)
        if gregorian_birth_date > datetime.now() - timedelta(days=365 * 18):
            raise ValidationException("Customer age cannot be less than 18 years")

        customer_code = dic['national_number']
        if customer_code is None or customer_code == 'None' or not customer_code.isdigit():
            raise ValidationException("Customer Code is not ok")
        c = RealCustomerInformation(type=dic['type'], customer_code=dic['national_number'],
                                    name=dic['name'], last_name=dic['last_name'], father_name=dic['father_name'],
                                    bc_number=dic['bc_number'], bc_serial_number=dic['bc_serial_number'],
                                    birth_date=gregorian_birth_date, bc_place_id=dic['bc_place_id'],
                                    birth_place_id=dic['birth_place_id'], gender=dic['gender'])

        return c


class ContactInformation(models.Model):
    class Meta:
        app_label = 'customer'

    customer = models.OneToOneField(RealCustomerInformation, related_name='contact_info', primary_key=True)
    phone_number = models.CharField(max_length=16)
    cell_number = models.CharField(max_length=16)
    email = models.EmailField()
    address = models.CharField(max_length=300)
    town = models.ForeignKey(Town)
    province = models.ForeignKey(Province)
    postal_code = models.CharField(max_length=20)

    @staticmethod
    def from_dic(dic):
        c = ContactInformation(
            customer_id=dic["customer_id"],
            phone_number=dic["phone_number"], cell_number=dic["cell_number"], email=dic["email"],
            address=dic["email"], town_id=dic['town_id'], province_id=dic['province_id'],
            postal_code=dic['postal_code'])
        return c


class JobInformation(models.Model):
    class Meta:
        app_label = 'customer'

    customer = models.OneToOneField(RealCustomerInformation, related_name='job_info', primary_key=True)
    job = models.ForeignKey(JobType)
    # job_activity = models.ForeignKey(max_length=100)
    Job_certificate = models.ForeignKey(JobCertificateType)
    job_certificate_number = models.CharField(max_length=25)
    job_province = models.ForeignKey(Province)
    job_town = models.ForeignKey(Town)
    job_contact_number = models.CharField(max_length=30)
    job_postal_code = models.CharField(max_length=30)
    job_address = models.CharField(max_length=700)

    @staticmethod
    def from_dic(dic):
        j = JobInformation(
            customer_id=dic['customer_id'],
            job_id=dic['job_id'],
            # job_activity=dic['job_activity'],
            Job_certificate_id=dic["Job_certificate_id"],
            job_certificate_number=dic["job_certificate_number"],
            job_province_id=dic[
                "job_province_id"], job_town_id=
            dic["job_town_id"],
            job_contact_number=dic['job_contact_number'], job_address=dic['job_address'],
            job_postal_code=dic['job_postal_code'])
        return j


class AssetInformation(models.Model):
    class Meta:
        app_label = 'customer'

    customer = models.OneToOneField(RealCustomerInformation, related_name='asset_info', primary_key=True)
    cash = models.BigIntegerField(default=0)
    account = models.BigIntegerField(default=0)
    business_place = models.ForeignKey(BusinessPlace)
    business_place_value = models.BigIntegerField(default=0)
    individual_credit_amount = models.BigIntegerField(default=0)
    company_credit_amount = models.BigIntegerField(default=0)
    manghool_value = models.BigIntegerField(default=0)
    no_manghool_value = models.BigIntegerField(default=0)
    vehicles_value = models.BigIntegerField(default=0)
    individual_debit_amount = models.BigIntegerField(default=0)
    company_debit_amount = models.BigIntegerField(default=0)
    bank_debit_amount = models.BigIntegerField(default=0)

    @staticmethod
    def from_dic(dic):
        asset = AssetInformation(
            customer_id=dic['customer_id'],
            cash=dic['cash'],
            account=dic['account'],
            business_place_id=dic['business_place_id'],
            business_place_value=dic['business_place_value'],
            individual_credit_amount=dic['individual_credit_amount'],
            company_credit_amount=dic['company_credit_amount'],
            manghool_value=dic['manghool_value'],
            no_manghool_value=dic['no_manghool_value'],
            vehicles_value=dic['vehicles_value'],
            individual_debit_amount=dic['individual_debit_amount'],
            company_debit_amount=dic['company_debit_amount'],
            bank_debit_amount=dic['bank_debit_amount']

        )
        return asset


class BankIncomeInformation(models.Model):
    class Meta:
        app_label = 'customer'

    customer = models.OneToOneField(RealCustomerInformation, related_name='bank_income_info', primary_key=True)

    income = models.IntegerField()

    @staticmethod
    def from_dic(dic):
        bi = BankIncomeInformation(income=dic['income'], customer_id=dic['customer_id'])
        return bi








