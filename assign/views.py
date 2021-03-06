# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.views.generic import View
from rose_config.response import *
from start_grant.models import Request
from assign.models import EnquiryAction, EnquiryAssign, EnquiryAssignResponse, EnquiryActionResponse, \
    AssignHistoryItemInstance
from utils.date_utils import greg_date_from_shamsi
from datetime import datetime
from django.utils.translation import ugettext as _


class EnquiryAssignView(View):
    def get(self, request, request_id, msg=None):
        if request.user.profile.role.name != 'superior':
            return HttpResponse('No Access')

        customer_request = Request.objects.get(id=request_id)
        existed_enquiry_assign = EnquiryAssign.objects.filter(request__id=1).count() > 0

        # Currently every request should have just one enquiry assign
        if existed_enquiry_assign:
            return HttpResponseRedirect('superior:tasks')

        selectable_actions = EnquiryAction.objects.filter(customer_type=customer_request.type)
        special_actions = EnquiryAction.objects.filter(customer_type='special')
        guarantor_action = None
        account_related_action = None
        if customer_request.need_guarantor():
            guarantor_action = EnquiryAction.objects.get(customer_type='conditional', id=20)

        if customer_request.complete_information.loan_type.name == 'foroosh-aghsati':
            account_related_action = EnquiryAction.objects.get(customer_type='conditional', id=18)

        candidate_target_users = User.objects.filter(profile__branch_code=request.user.profile.branch_code,
                                                     profile__role__name='teller')

        template = loader.get_template('enquiry_assign.html')
        context = RequestContext(request, {'request_id': request_id,
                                           'actions': selectable_actions,
                                           'special_actions': special_actions,
                                           'target_users': candidate_target_users,
                                           'guarantor_action': guarantor_action,
                                           'account_related_action': account_related_action,
                                           'error_message': msg})
        return HttpResponse(template.render(context))


    def post(self, request, request_id):
        if request.user.profile.role.name != 'superior':
            return HttpResponse('No Access')

        customer_request = Request.objects.get(id=request_id)
        expire_date = greg_date_from_shamsi(request.POST['expire_date'], '/')
        if expire_date < datetime.now():
            return self.get(request, request_id, msg=_("Expire date cannot be less than today"))

        assign = EnquiryAssign()
        assign.source_id = request.user.id
        assign.target_id = request.POST['target_user']
        assign.comment = request.POST['comment']
        assign.priority = request.POST['priority']
        assign.expire_date = expire_date
        assign.request_id = request_id
        assign.save()
        for item in request.POST.getlist('selected_actions'):
            assign.actions.add(int(item))

        for item in request.POST.getlist('selected_special_actions'):
            assign.actions.add(int(item))

        customer_request.status = 'enquiry_assigned'
        customer_request.save()

        return HttpResponseRedirect(reverse('superior:tasks'))


class EnquiryResponseView(View):
    def get(self, request, assign_id):
        assign = EnquiryAssign.objects.get(id=int(assign_id))
        if assign.target_id != request.user.id:
            return HttpResponseRedirect(reverse('grant:track'))
        if assign.status == 'done':
            return HttpResponseRedirect(reverse('notification:list'))
        if not hasattr(assign, 'response'):
            history_item = AssignHistoryItemInstance()
            history_item.history_item_id = "see"
            history_item.issue_date = datetime.now()
            history_item.save()
            assign.history.items.add(history_item)

            response = EnquiryAssignResponse()
            response.enquiry_assign = assign
            response.save()
        else:
            response = assign.response
        if response.action_responses.count() < assign.actions.count():
            for action in assign.actions.all():
                # if not hasattr(action, 'response'):
                action_response = EnquiryActionResponse()
                action_response.action = action
                response.action_responses.add(action_response)

        template = loader.get_template('enquiry_response.html')
        context = RequestContext(request, {'assign': assign})

        return HttpResponse(template.render(context))

    def post(self, request, assign_id):
        assign = EnquiryAssign.objects.get(id=int(assign_id))
        assign.response.comment = request.POST.get("comment", "")
        assign.response.complete()
        return HttpResponseRedirect(reverse('grant:track'))


class EnquiryResponseStatusView(View):
    def get(self, request, request_id):
        enquiry_assgin = EnquiryAssign.objects.filter(request__id=request_id).last()

        template = loader.get_template('enquiry_response_status.html')
        context = RequestContext(request, {'enquiry_assign': enquiry_assgin})
        return HttpResponse(template.render(context))


class EnquiryActionResponseStartView(View):
    def post(self, request):
        action_response_id = int(request.POST.get("action_response_id"))
        action_response = EnquiryActionResponse.objects.get(id=action_response_id)
        if action_response.response.enquiry_assign.target_id == request.user.id:
            action_response.start()
            action_response.save()
            return generate_ok_response()

        else:
            return generate_error_response()


class EnquiryActionResponseStopView(View):
    def post(self, request):
        action_response_id = int(request.POST.get("action_response_id"))
        action_response = EnquiryActionResponse.objects.get(id=action_response_id)
        if action_response.response.enquiry_assign.target_id == request.user.id:
            action_response.stop()
            action_response.save()
            return generate_ok_response()

        else:
            return generate_error_response()


class EnquiryActionResponseCompleteView(View):
    def post(self, request):
        action_response_id = int(request.POST.get("action_response_id"))
        action_response = EnquiryActionResponse.objects.get(id=action_response_id)
        if action_response.response.enquiry_assign.target_id == request.user.id:
            accepted = (request.POST.get('accepted', 'False') == 'True')
            reference_number = request.POST.get('reference_number', '0')
            action_response.reference_number = reference_number
            # str(reference_number)
            action_response.comment = request.POST.get('comment', '')
            action_response.accepted = accepted
            action_response.complete()
            action_response.save()
            return generate_ok_response()

        else:
            return generate_error_response()