from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, RequestContext
from django.views.generic import View
from start_grant.models import Request
from superior.models import EnquiryAction


class TaskListView(View):
    def get(self, request):
        if request.user.profile.role.name != 'superior':
            return HttpResponse('No Access')
        template = loader.get_template('tasks_list.html')
        requests = Request.objects.filter(status='checklist_completed', branch_code=request.user.profile.branch_code)
        context = RequestContext(request, {'requests': requests})
        return HttpResponse(template.render(context))


class EnquiryAssignView(View):
    def get(self, request, request_id):
        if request.user.profile.role.name != 'superior':
            return HttpResponse('No Access')

        customer_request = Request.objects.get(id=request_id)
        selectable_actions = EnquiryAction.objects.filter(customer_type=customer_request.type)

        candidate_target_users = User.objects.filter(profile__branch_code=request.user.profile.branch_code,
                                                     profile__role__name='teller')

        template = loader.get_template('enquiry_assign.html')
        context = RequestContext(request, {'actions': selectable_actions, 'target_users': candidate_target_users})

        return HttpResponse(template.render(context))