from django.contrib.auth.models import User
from django.db import models
from customer.models.common import CUSTOMER_TYPE
from start_grant.models import Request
from jdatetime import datetime as jalali_datetime


class EnquiryAction(models.Model):
    customer_type = models.CharField(max_length=30, choices=CUSTOMER_TYPE)
    name = models.CharField(max_length=200)
    local_name = models.CharField(max_length=500)


class AssignType(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    local_name = models.CharField(max_length=200)


class Assign(models.Model):
    source = models.ForeignKey(User, related_name='assigned_sources')
    target = models.ForeignKey(User, related_name='assigned_targets')
    issue_date = models.DateTimeField(auto_now=True)
    expire_date = models.DateTimeField()
    comment = models.CharField(max_length=1000)
    priority = models.IntegerField(max_length=30)
    assign_type = models.ForeignKey(AssignType, related_name='assigns')


    def get_persian_issue_date(self):
        return jalali_datetime.fromgregorian(datetime=self.issue_date).strftime('%Y/%m/%d')

    def get_persian_expire_date(self):
        return jalali_datetime.fromgregorian(datetime=self.expire_date).strftime('%Y/%m/%d')


class EnquiryAssign(Assign):
    def __init__(self):
        self.assign_type = 'enquiry'

    actions = models.ManyToManyField(EnquiryAction)
    request = models.ForeignKey(Request, related_name='enquiry_assigns')
    # special_actions

