from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from customer.models.common import CUSTOMER_TYPE
from start_grant.models import Request
from jdatetime import datetime as jalali_datetime
from datetime import datetime


class EnquiryAction(models.Model):
    customer_type = models.CharField(max_length=30, choices=CUSTOMER_TYPE)
    name = models.CharField(max_length=200)
    local_name = models.CharField(max_length=500)


class AssignType(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    local_name = models.CharField(max_length=200)
    url = models.CharField(default="", max_length=200)


class Assign(models.Model):
    source = models.ForeignKey(User, related_name='assigned_sources')
    target = models.ForeignKey(User, related_name='assigned_targets')
    issue_date = models.DateTimeField(auto_now=True)
    expire_date = models.DateTimeField()
    comment = models.CharField(max_length=1000)
    priority = models.IntegerField(max_length=30)
    request = models.ForeignKey(Request, related_name='enquiry_assigns')
    assign_type = models.ForeignKey(AssignType, related_name='assigns')


    def get_persian_issue_date(self):
        return jalali_datetime.fromgregorian(datetime=self.issue_date).strftime('%Y/%m/%d')

    def get_persian_expire_date(self):
        return jalali_datetime.fromgregorian(datetime=self.expire_date).strftime('%Y/%m/%d')


class AssignHistoryItem(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    local_name = models.CharField(max_length=200)


class AssignHistoryItemInstance(models.Model):
    history_item = models.ForeignKey(AssignHistoryItem)
    issue_date = models.DateTimeField()
    comment = models.CharField(max_length=1000, default='')


class AssignHistory(models.Model):
    assign = models.OneToOneField(Assign)
    items = models.ManyToManyField(AssignHistoryItemInstance)

    def last_item(self):
        return self.items.last()


class EnquiryAssign(Assign):
    def __init__(self, *args, **kwargs):
        super(EnquiryAssign, self).__init__(*args, **kwargs)
        self.assign_type_id = 'enquiry'

    actions = models.ManyToManyField(EnquiryAction)


class EnquiryAssignResponse(models.Model):
    enquiry_assign = models.OneToOneField(EnquiryAssign, related_name='response')
    comment = models.CharField(max_length=1000)
    status = models.CharField(max_length=200)
    end_date = models.DateTimeField(null=True, blank=True)
    accepted = models.BooleanField(default=False)

    def complete(self):
        if self.is_done() and self.is_accepted():
            self.status = 'done'
            self.end_date = datetime.now()
        else:
            raise Exception('Assign response is not ready for being complete')


    def is_done(self):
        for response in self.action_responses.all():
            if not response.status == 'done':
                return False
        return True

    def is_accepted(self):
        for response in self.action_responses.all():
            if not response.accepted:
                return False
            return True


class EnquiryActionResponse(models.Model):
    action = models.OneToOneField(EnquiryAction, related_name='response')
    comment = models.CharField(max_length=1000)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    #not_started
    #in_progress
    #stopped
    #done
    status = models.CharField(max_length=50, default='not_started')
    reference_number = models.CharField(max_length=20, null=True, blank=True)
    #The result of every action can be accepted or rejected
    accepted = models.BooleanField(default=False)
    response = models.ForeignKey(EnquiryAssignResponse, related_name='action_responses')


    def start(self):
        if self.status == 'done':
            raise Exception("action_response has been done before")
        if self.start_date is None or self.start_date == '':
            self.start_date = datetime.now()
        self.status = 'in_progress'

    def stop(self):
        if self.status == 'done':
            raise Exception("action_response has been done before")
        self.status = 'stopped'

    def complete(self):
        if self.status == 'done':
            raise Exception("action_response has been done before")
        self.end_date = datetime.now()
        self.status = 'done'


def create_assign_history(sender, instance, created, **kwargs):
    if not isinstance(instance, Assign):
        return
    if created:
        assign, is_new = AssignHistory.objects.get_or_create(assign=instance)
        if is_new:
            history_instance = AssignHistoryItemInstance()
            history_instance.history_item_id = 'create'
            history_instance.issue_date = datetime.now()
            history_instance.save()
            assign.items.add(history_instance)
            assign.save()


post_save.connect(create_assign_history)

