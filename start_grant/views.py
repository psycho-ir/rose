from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.views.generic import View
from rose_config.exceptions import ValidationException
from start_grant.models import Request, CheckList

__author__ = 'soroosh'

from rose_config.models import config, JobType, JobCertificateType, Province, Town, LoanType, RefundType, Bank, \
    VasigheType, BusinessPlace, BusinessPart, RequestDescription
from django.utils.translation import ugettext as _


class StartView(View):
    def get(self, request):
        haghighi_max_loan_amount = config.objects.get(pk='HAGHIGHI_MAX_LOAN_AMOUNT')
        hoghooghi_max_loan_amount = config.objects.get(pk='HOGHOOGHI_MAX_LOAN_AMOUNT')
        business_parts = BusinessPart.objects.all()
        request_descriptions = RequestDescription.objects.filter(business_parts=business_parts.first().id)

        template = loader.get_template("start.html")
        context = RequestContext(request,
                                 {
                                     'business_parts': business_parts, 'request_descriptions': request_descriptions,
                                     'haghighi_max_loan_amount': haghighi_max_loan_amount,
                                     'hoghooghi_max_loan_amount':
                                         hoghooghi_max_loan_amount})
        return HttpResponse(template.render(context))

    def post(self, request):
        try:
            request = Request.from_dic(request.POST, request.user)
        except ValidationException as e:
            haghighi_max_loan_amount = config.objects.get(pk='HAGHIGHI_MAX_LOAN_AMOUNT')
            hoghooghi_max_loan_amount = config.objects.get(pk='HOGHOOGHI_MAX_LOAN_AMOUNT')
            business_parts = BusinessPart.objects.all()
            request_descriptions = RequestDescription.objects.filter(business_parts=business_parts.first().id)

            template = loader.get_template("start.html")
            context = RequestContext(request,
                                     {
                                         'error_message': _(e.message),
                                         'business_parts': business_parts, 'request_descriptions': request_descriptions,
                                         'haghighi_max_loan_amount': haghighi_max_loan_amount,
                                         'hoghooghi_max_loan_amount':
                                             hoghooghi_max_loan_amount})
            return HttpResponse(template.render(context))

        request.save()

        if request.type == 'haghighi':
            return HttpResponseRedirect(
                reverse('customer:real_register') + '?customer_id=' + request.cif + '&next=' + reverse('grant:submit',
                                                                                                       args=(
                                                                                                       request.id,)))

        if request.type == 'hoghooghi':
            return HttpResponseRedirect(reverse('customer:enterprise', args=(request.cif,)))

        return HttpResponse("Fatal Error %s" % request.type)


class CheckListView(View):
    def get(self, request, request_id):
        checklist = CheckList.objects.get(request__id=request_id)
        readonly = False
        if checklist.request.user_id != request.user.id:
            readonly = True

        template = loader.get_template('check_list.html')
        context = RequestContext(request, {'readonly': readonly, 'request_id': request_id,
                                           'checkListItems': checklist.items.all()})
        return HttpResponse(template.render(context))

    def post(self, request, request_id):
        checklist = CheckList.objects.get(request__id=request_id)
        for item in checklist.items.all():
            value = bool(request.POST.get(str(item.id), False))
            item.checked = value
            item.save()

        if checklist.is_done():
            customer_request = Request.objects.get(id=request_id)
            customer_request.status = 'checklist_completed'
            customer_request.save()

        return HttpResponseRedirect(reverse('grant:track'))