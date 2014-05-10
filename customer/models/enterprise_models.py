from django.db import models
from jdatetime import datetime as jalali_datetime
from customer.models import Customer
from customer.models.real_models import RealCustomerInformation
from rose_config.models import CompanyType, Province, Town, JobCertificateType
from utils.date_utils import greg_date_from_shamsi

__author__ = 'soroosh'


class BoadOfDirectorRole(models.Model):
    class Meta:
        app_label = 'customer'

    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60, default="")
    enable = models.BooleanField(default=True)


class RegisterTown(models.Model):
    class Meta:
        app_label = 'customer'

    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60, default="")
    enable = models.BooleanField(default=True)


class EnterpriseCustomerInformation(Customer):
    class Meta:
        app_label = 'customer'

    company_name = models.CharField(max_length=256)
    register_number = models.IntegerField()
    company_type = models.ForeignKey(CompanyType)
    register_date = models.DateTimeField()
    newspaper_number = models.IntegerField()
    newspaper_date = models.DateTimeField()
    register_place = models.ForeignKey(RegisterTown)

    def get_persian_register_date(self):
        return jalali_datetime.fromgregorian(datetime=self.register_date).strftime('%Y/%m/%d')

    def get_persian_newspaper_date(self):
        return jalali_datetime.fromgregorian(datetime=self.newspaper_date).strftime('%Y/%m/%d')

    @staticmethod
    def from_dic(dic):
        print dic
        register_date = greg_date_from_shamsi(dic['register_date'], '/')
        print register_date
        newspaper_date = greg_date_from_shamsi(dic['newspaper_date'], '/')
        c = EnterpriseCustomerInformation(
            customer_code=dic['company_id'],
            company_name=dic['company_name'],
            register_number=dic['register_number'],
            company_type_id=dic['company_type_id'],
            register_date=register_date,
            newspaper_number=dic['newspaper_number'],
            newspaper_date=newspaper_date,
            register_place_id=dic['register_place_id']
        )

        return c


class BoardOfDirector(models.Model):
    class Meta:
        app_label = 'customer'

    company = models.ForeignKey(EnterpriseCustomerInformation)
    customer = models.ForeignKey(RealCustomerInformation)
    role = models.ForeignKey(BoadOfDirectorRole)
    sign_permission = models.BooleanField(default=False)
    sign_expire_date = models.DateField()
    sign_enough = models.BooleanField(default=False)

    @staticmethod
    def from_dic(dic):
        b = BoardOfDirector(company_id=dic['company_id'],
                            customer_id=dic['customer_id'],
                            role_id=dic['role_id'],
                            sing_permission=dic['sign_permission'],
                            sign_expire_date=dic['sign_expire_date'],
                            sign_enough=dic['sign_enough']
        )

        return b


class EnterpriseContactInformation(models.Model):
    class Meta:
        app_label = 'customer'

    company = models.OneToOneField(EnterpriseCustomerInformation, related_name='contact_info', primary_key=True)
    province = models.ForeignKey(Province)
    town = models.ForeignKey(Town)
    address = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    postal_code = models.CharField(max_length=14)

    @staticmethod
    def from_dic(dic):
        c = EnterpriseContactInformation(company_id=dic['company_id'],
                                         province_id=dic['province_id'],
                                         town_id=dic['town_id'],
                                         address=dic['address'],
                                         phone_number=dic['phone_number'],
                                         email=dic['email'],
                                         postal_code=dic['postal_code']
        )
        return c


class EnterpriseActivity(models.Model):
    class Meta:
        app_label = 'customer'

    company = models.OneToOneField(EnterpriseCustomerInformation, related_name='activity_info', primary_key=True)
    activity_type = models.CharField(max_length=256)
    certificate_type = models.ForeignKey(JobCertificateType)
    certificate_number = models.CharField(max_length=20)
    certificate_start_date = models.DateTimeField()
    certificate_expire_date = models.DateTimeField()

    def get_persian_certificate_start_date(self):
        return jalali_datetime.fromgregorian(datetime=self.certificate_start_date).strftime('%Y/%m/%d')

    def get_persian_certificate_expire_date(self):
        return jalali_datetime.fromgregorian(datetime=self.certificate_expire_date).strftime('%Y/%m/%d')

    @staticmethod
    def from_dic(dic):
        certificate_start_date = greg_date_from_shamsi(dic['certificate_start_date'], '/')
        certificate_expire_date = greg_date_from_shamsi(dic['certificate_expire_date'], '/')
        ea = EnterpriseActivity(
            company_id=dic['company_id'],
            activity_type=dic['activity_type'],
            certificate_type_id=dic['certificate_type_id'],
            certificate_number=dic['certificate_number'],
            certificate_start_date=certificate_start_date,
            certificate_expire_date=certificate_expire_date
        )

        return ea






