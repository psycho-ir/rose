from django.db import models


class config(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=500)
    value = models.CharField(max_length=500)


class Province(models.Model):
    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60, default="")
    enable = models.BooleanField(default=True)

    class Meta:
        ordering = ['local_name']


class BusinessPart(models.Model):
    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60, default="")
    enable = models.BooleanField(default=True)


class RequestDescription(models.Model):
    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60, default="")
    enable = models.BooleanField(default=True)
    business_parts = models.ManyToManyField(to=BusinessPart, db_constraint=True,
                                            related_name='request_descriptions')


class RefundType(models.Model):
    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60)
    enable = models.BooleanField(default=True)


class CreditType(models.Model):
    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60, default="")
    enable = models.BooleanField(default=True)


class LoanType(models.Model):
    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60, default="")
    enable = models.BooleanField(default=True)
    refund_types = models.ManyToManyField(RefundType)
    credit_type = models.ForeignKey(CreditType, related_name='loan_types')


class LoanPolicy(models.Model):
    loan_type = models.OneToOneField(LoanType, related_name='policy')
    real_max_duration = models.IntegerField(default=90)  # Unit is month
    real_max_amount = models.BigIntegerField(default=99999999999)

    enterprise_max_duration = models.IntegerField(default=90)
    enterprise_max_amount = models.BigIntegerField(default=999999999)


class Town(models.Model):
    class Meta:
        ordering = ['local_name']

    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60)
    enable = models.BooleanField(default=True)
    province = models.ForeignKey(Province)


class JobType(models.Model):
    business_part = models.ForeignKey(BusinessPart)
    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60)
    enable = models.BooleanField(default=True)


# class JobActivityType(models.Model):
# name = models.CharField(max_length=50)
# local_name = models.CharField(max_length=50)
# description = models.CharField(max_length=60)
# enable = models.BooleanField(default=True)


class JobCertificateType(models.Model):
    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60, default="")
    enable = models.BooleanField(default=True)
    type = models.CharField(default='haghighi', max_length=20)
    business_part = models.ManyToManyField(BusinessPart)


class BusinessPlace(models.Model):
    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60, default="")
    enable = models.BooleanField(default=True)


class Bank(models.Model):
    class Meta:
        ordering = ['local_name']

    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60, default="")
    enable = models.BooleanField(default=True)


class VasigheCategory(models.Model):
    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60, default="")
    enable = models.BooleanField(default=True)


class VasigheType(models.Model):
    category = models.ForeignKey(VasigheCategory, related_name='vasighe_types')
    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60, default="")
    nesbat_naghd_shavandegi = models.SmallIntegerField()
    # naghdi_value = models.SmallIntegerField()
    tarhin_value = models.SmallIntegerField()
    cover_value = models.SmallIntegerField()
    need_assessment = models.BooleanField(default=True)

    enable = models.BooleanField(default=True)


class CompanyType(models.Model):
    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60, default="")
    enable = models.BooleanField(default=True)