from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from jdatetime import datetime as jalali_datetime
from customer.models import Customer
from customer.models.real_models import RealCustomerInformation
from rose_config.exceptions import ValidationException
from rose_config.models import CompanyType, Province, Town, JobCertificateType
from utils.date_utils import greg_date_from_shamsi
from datetime import datetime

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

    def is_information_completed(self):
        if hasattr(self, 'contact_info') and hasattr(self, 'asset_info') and hasattr(self, 'activity_info'):
            return True
        return False

    @staticmethod
    def from_dic(dic):
        register_date = greg_date_from_shamsi(dic['register_date'], '/')
        newspaper_date = greg_date_from_shamsi(dic['newspaper_date'], '/')
        current_date = datetime.now()

        if newspaper_date < register_date:
            raise ValidationException("Newspaper date cannot be before register date")

        if newspaper_date >= current_date:
            raise ValidationException("Newspaper date cannot be after today")

        if register_date >= current_date:
            raise ValidationException("Register date cannot be after today")
        c = EnterpriseCustomerInformation(
            type='hoghooghi',
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
        unique_together = ('company', 'customer',)

    company = models.ForeignKey(EnterpriseCustomerInformation, related_name='director_set')
    customer = models.ForeignKey(RealCustomerInformation)
    role = models.ForeignKey(BoadOfDirectorRole)
    sign_permission = models.BooleanField(default=False)
    sign_expire_date = models.DateTimeField()
    sign_enough = models.BooleanField(default=False)

    def get_persian_sign_expire_date(self):
        return jalali_datetime.fromgregorian(datetime=self.sign_expire_date).strftime('%Y/%m/%d')

    @staticmethod
    def from_dic(dic):
        try:
            RealCustomerInformation.objects.get(customer_code=dic['customer_id'])
        except ObjectDoesNotExist as e:
            raise ValidationException("Real customer does not exist")

        sign_expire_date = greg_date_from_shamsi(dic['sign_expire_date'], '/')
        if datetime.now() > sign_expire_date:
            raise ValidationException("Sign expire date should be more than one month")
        if datetime.now().year == sign_expire_date.year and datetime.now().month >= sign_expire_date.month:
            raise ValidationException("Sign expire date should be more than one month")

        if BoardOfDirector.objects.filter(company_id=dic['company_id'], customer_id=dic['customer_id']).exists():
            b = BoardOfDirector.objects.get(company_id=dic['company_id'], customer_id=dic['customer_id'])
        else:
            b = BoardOfDirector(company_id=dic['company_id'], customer_id=dic['customer_id'])
        b.role_id = dic['role_id']
        b.sign_permission = dic.get('sign_permission', False)
        b.sign_expire_date = sign_expire_date
        b.sign_enough = dic.get('sign_enough', False)

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

    company = models.ForeignKey(EnterpriseCustomerInformation, related_name='activity_info')
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
        if certificate_start_date >= certificate_expire_date:
            raise ValidationException("Expire date cannot be lower than start date")
        import datetime

        if certificate_expire_date < datetime.datetime.now():
            raise ValidationException("Certificate expired")
        ea = EnterpriseActivity(
            company_id=dic['company_id'],
            activity_type=dic['activity_type'],
            certificate_type_id=dic['certificate_type_id'],
            certificate_number=dic['certificate_number'],
            certificate_start_date=certificate_start_date,
            certificate_expire_date=certificate_expire_date
        )

        return ea


class EnterpriseAssetInformation(models.Model):
    class Meta:
        app_label = 'customer'

    company = models.OneToOneField(EnterpriseCustomerInformation, related_name='asset_info', primary_key=True)

    cash = models.BigIntegerField(default=0)
    account = models.BigIntegerField(default=0)

    ingredient = models.BigIntegerField(default=0)
    current_develop_products_amount = models.BigIntegerField(default=0)
    current_products_amount = models.BigIntegerField(default=0)

    individual_credit_amount = models.BigIntegerField(default=0)
    company_credit_amount = models.BigIntegerField(default=0)
    other_credit_amount = models.BigIntegerField(default=0)

    manghool_building_amount = models.BigIntegerField(default=0)
    manghool_installation_amount = models.BigIntegerField(default=0)
    manghool_vehicle_amount = models.BigIntegerField(default=0)

    oragh_mosharekat_bi_nam_amount = models.BigIntegerField(default=0)
    oragh_saham_sherkat_amount = models.BigIntegerField(default=0)
    sahm_sherke_amount = models.BigIntegerField(default=0)

    registered_payed = models.BigIntegerField(default=0)
    registered_guarantied = models.BigIntegerField(default=0)

    remained_benefit_amount = models.BigIntegerField(default=0)

    loan_from_individual_amount = models.BigIntegerField(default=0)
    loan_from_institutes_amount = models.BigIntegerField(default=0)
    loan_from_banks_amount = models.BigIntegerField(default=0)

    pish_daryaft_amount = models.BigIntegerField(default=0)
    bestankaran_amount = models.BigIntegerField(default=0)

    payed_documents_amount = models.BigIntegerField(default=0)

    @staticmethod
    def from_dic(dic):
        asset = EnterpriseAssetInformation(company_id=dic['company_id'],
                                           cash=dic['cash'],
                                           account=dic['account'],
                                           ingredient=dic['ingredient'],
                                           current_develop_products_amount=dic['current_develop_products_amount'],
                                           current_products_amount=dic['current_products_amount'],
                                           individual_credit_amount=dic['individual_credit_amount'],
                                           company_credit_amount=dic['company_credit_amount'],
                                           other_credit_amount=dic['other_credit_amount'],
                                           manghool_building_amount=dic['manghool_building_amount'],
                                           manghool_installation_amount=dic['manghool_installation_amount'],
                                           manghool_vehicle_amount=dic['manghool_vehicle_amount'],
                                           oragh_mosharekat_bi_nam_amount=dic['oragh_mosharekat_bi_nam_amount'],
                                           oragh_saham_sherkat_amount=dic['oragh_saham_sherkat_amount'],
                                           sahm_sherke_amount=dic['sahm_sherke_amount'],
                                           registered_payed=dic['registered_payed'],
                                           registered_guarantied=dic['registered_guarantied'],
                                           remained_benefit_amount=dic['remained_benefit_amount'],
                                           loan_from_individual_amount=dic['loan_from_individual_amount'],
                                           loan_from_institutes_amount=dic['loan_from_institutes_amount'],
                                           loan_from_banks_amount=dic['loan_from_banks_amount'],
                                           pish_daryaft_amount=dic['pish_daryaft_amount'],
                                           bestankaran_amount=dic['bestankaran_amount'],
                                           payed_documents_amount=dic['payed_documents_amount']
        )
        return asset







