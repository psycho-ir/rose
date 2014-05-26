from django.db.models import Q
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.views.generic import View
from start_grant.models import Request


class TaskListView(View):
    def get(self, request):
        if request.user.profile.role.name != 'superior':
            return HttpResponse('No Access')
        template = loader.get_template('tasks_list.html')
        requests = Request.objects.filter(Q(status='checklist_completed') | Q(status='enquiry_assigned')
                                          | Q(status='enquiry_assign_completed'),
                                          branch_code=request.user.profile.branch_code)

        context = RequestContext(request, {'requests': requests})
        return HttpResponse(template.render(context))
