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
#     name = models.CharField(max_length=50)
#     local_name = models.CharField(max_length=50)
#     description = models.CharField(max_length=60)
#     enable = models.BooleanField(default=True)


class JobCertificateType(models.Model):
    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60, default="")
    enable = models.BooleanField(default=True)


class BusinessPlace(models.Model):
    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60, default="")
    enable = models.BooleanField(default=True)


class Bank(models.Model):
    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60, default="")
    enable = models.BooleanField(default=True)


class VasigheType(models.Model):
    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60, default="")
    enable = models.BooleanField(default=True)


class CompanyType(models.Model):
    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50)
    description = models.CharField(max_length=60, default="")
    enable = models.BooleanField(default=True)