from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader, RequestContext
from django.views.generic import View
from start_grant.models import Request
from assign.models import EnquiryAction, EnquiryAssign, EnquiryAssignResponse, EnquiryActionResponse
from utils.date_utils import greg_date_from_shamsi


class EnquiryAssignView(View):
    def get(self, request, request_id):
        if request.user.profile.role.name != 'superior':
            return HttpResponse('No Access')

        customer_request = Request.objects.get(id=request_id)
        selectable_actions = EnquiryAction.objects.filter(customer_type=customer_request.type)
        special_actions = EnquiryAction.objects.filter(customer_type='special')

        candidate_target_users = User.objects.filter(profile__branch_code=request.user.profile.branch_code,
                                                     profile__role__name='teller')
        template = loader.get_template('enquiry_assign.html')
        context = RequestContext(request, {'request_id': request_id,
                                           'actions': selectable_actions,
                                           'special_actions': special_actions,
                                           'target_users': candidate_target_users})
        return HttpResponse(template.render(context))


    def post(self, request, request_id):
        if request.user.profile.role.name != 'superior':
            return HttpResponse('No Access')

        customer_request = Request.objects.get(id=request_id)
        expire_date = greg_date_from_shamsi(request.POST['expire_date'], '/')
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
        if not hasattr(assign, 'response'):
            response = EnquiryAssignResponse()
            response.enquiry_assign = assign
            response.save()
        else:
            response = assign.response
        for action in assign.actions.all():
            if not hasattr(action, 'response'):
                action_response = EnquiryActionResponse()
                action_response.action = action
                response.action_responses.add(action_response)

        template = loader.get_template('enquiry_response.html')
        context = RequestContext(request, {'assign': assign})

        return HttpResponse(template.render(context))


class EnquiryActionResponseStartView(View):
    def post(self, request):
        action_response_id = int(request.POST.get("action_response_id"))
        action_response = EnquiryActionResponse.objects.get(id=action_response_id)
        if action_response.response.enquiry_assign.target_id == request.user.id:
            action_response.start()
            action_response.save()
            return HttpResponse("True")

        else:
            return HttpResponse("False")