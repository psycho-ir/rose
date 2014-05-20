from django.contrib.auth.models import User
from django.db import models
from customer.models.common import CUSTOMER_TYPE
from start_grant.models import Request


class EnquiryAction(models.Model):
    customer_type = models.CharField(max_length=30, choices=CUSTOMER_TYPE)
    name = models.CharField(max_length=200)
    local_name = models.CharField(max_length=500)


class Assign(models.Model):
    source = models.ForeignKey(User, related_name='assigned_sources')
    target = models.ForeignKey(User, related_name='assigned_targets')
    issue_date = models.DateTimeField(auto_now=True)
    expire_date = models.DateTimeField()
    comment = models.CharField(max_length=1000)
    priority = models.IntegerField(max_length=30)


class EnquiryAssign(Assign):
    actions = models.ManyToManyField(EnquiryAction)
    request = models.ForeignKey(Request, related_name='enquiry_assigns')
    # special_actions

