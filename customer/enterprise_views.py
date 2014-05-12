from django.http.response import HttpResponse
from django.views.generic import View
from customer.models.enterprise_models import *

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


class EnterpriseAssetInfoView(View):
    def post(self, request):
        try:
            asset = EnterpriseAssetInformation.from_dic(request.POST)
            asset.save()
            return HttpResponse("True")
        except Exception as e:
            print e
            return HttpResponse("False")
