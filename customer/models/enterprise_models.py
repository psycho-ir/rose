from django.db import models
from customer.models import Customer
from customer.models.real_models import RealCustomerInformation
from rose_config.models import CompanyType, Province, Town, JobCertificateType

__author__ = 'soroosh'


class BoadOfDirectorRole(models.Model):
    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60, default="")
    enable = models.BooleanField(default=True)


class RegisterTown(models.Model):
    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60, default="")
    enable = models.BooleanField(default=True)


class EnterpriseCustomerInformation(Customer):
    company_name = models.CharField(max_length=256)
    register_number = models.IntegerField()
    company_type = models.ForeignKey(CompanyType)
    register_date = models.DateField()
    newspaper_number = models.IntegerField()
    newspaper_date = models.DateField()
    register_place = models.ForeignKey(RegisterTown)

    @staticmethod
    def from_dic(dic):
        c = EnterpriseCustomerInformation(company_name=dic['company_name'],
                                          register_number=dic['register_number'],
                                          company_type=dic['company_type'],
                                          register_date=dic['register_date'],
                                          newspaper_number=dic['newspaper_number'],
                                          newspaper_date=dic['newspaper_date'],
                                          register_place=dic['register_place']
        )

        return c


class BoardOfDirector(models.Model):
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
    company = models.OneToOneField(EnterpriseCustomerInformation, primary_key=True)
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
    activity_type = models.CharField(max_length=256)
    certificate_type = models.ForeignKey(JobCertificateType)
    certificate_number = models.CharField(max_length=20)
    certificate_start_date = models.DateField()
    certificate_expire_date = models.DateField()

    @staticmethod
    def from_dic(dic):
        ea = EnterpriseActivity(
            activity_type=dic['activity_type'],
            certificate_type=dic['certificate_type'],
            certificate_number=dic['certificate_number'],
            certificate_start_date=dic['certificate_start_date'],
            certificate_expire_date=dic['certificate_expire_date']
        )

        return ea






