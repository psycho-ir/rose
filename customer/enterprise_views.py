from time import sleep
from django.core import serializers
from django.http.response import HttpResponse
from django.views.generic import View
from customer.models.enterprise_models import *
import json

__author__ = 'soroosh'


class EnterpriseCustomerInfoView(View):
    def post(self, request):
        try:
            customer = EnterpriseCustomerInformation.from_dic(request.POST)
            customer.save()

            return HttpResponse("True")

        except Exception as e:
            print e
            return HttpResponse("False")


class BoardOfDirectorView(View):
    def post(self, request):
        try:
            board = BoardOfDirector.from_dic(request.POST)
            board.save()

            return HttpResponse("True")

        except Exception as e:
            print e
            return HttpResponse("False")


class BoardOfDirectorListView(View):
    def get(self, request):
        company_id = request.GET.get('company_id')
        directors = BoardOfDirector.objects.filter(company_id=company_id)

        result = []
        for d in directors:
            result.append({'national_number': d.customer.customer_code,
                           'name': d.customer.name,
                           'last_name': d.customer.last_name,
                           'role': d.role.local_name,
                           'sign_permission': d.sign_permission,
                           'sign_enough': d.sign_enough,
                           'sign_expire_date': d.get_persian_sign_expire_date(),
                           'role_id': d.role_id})
        encoded = json.dumps(result)

        return HttpResponse(encoded)


class EnterpriseContactInformationView(View):
    def post(self, request):
        try:
            contact = EnterpriseContactInformation.from_dic(request.POST)
            contact.save()

            return HttpResponse("True")

        except Exception as e:
            print e
            return HttpResponse("False")


class EnterpriseActivityView(View):
    def post(self, request):
        try:
            activity = EnterpriseActivity.from_dic(request.POST)
            activity.save()

            return HttpResponse("True")

        except Exception as e:
            print e
            return HttpResponse("False")


class EnterpriseActivityListView(View):
    def get(self, request):
        company_id = request.GET.get('company_id')
        activities = list(EnterpriseActivity.objects.filter(company_id=company_id))
        result = []
        for a in activities:
            result.append({'activity_type': a.activity_type,
                           'certificate_name': a.certificate_type.local_name,
                           'certificate_number': a.certificate_number,
                           'register_date': a.get_persian_certificate_start_date(),
                           'expire_date': a.get_persian_certificate_expire_date(),
                           'activity_id': a.id,
                           'company_id': a.company_id
            })

        encoded = json.dumps(result, sort_keys=False)
        print encoded
        return HttpResponse(encoded)


class EnterpriseActivityDeleteView(View):
    def get(self, request):
        try:
            activity = EnterpriseActivity.objects.get(company_id=request.GET.get('company_id'),
                                                      id=request.GET.get('activity_id'))
            print activity
            activity.delete()
            return HttpResponse("True")
        except Exception as e:
            print e
            return HttpResponse("False")


class EnterpriseAssetInfoView(View):
    def post(self, request):
        try:
            asset = EnterpriseAssetInformation.from_dic(request.POST)
            asset.save()
            return HttpResponse("True")
        except Exception as e:
            print e
            return HttpResponse("False")
