from django.db import transaction
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from customer.models import CustomerInformation, ContactInformation, JobInformation, BankIncomeInformation, \
    SanadMelkiInformation, AssetInformation
from rose_config.models import VasigheType


class CustomerInfoView(View):
    def post(self, request):
        try:
            customer_info = CustomerInformation.from_dic(request.POST)
            customer_info.save()
            return HttpResponse("True")

        except Exception as e:
            print(e)
            return HttpResponse("False")


class ContactInfoView(View):
    def post(self, request):
        try:
            contact_info = ContactInformation.from_dic(request.POST)
            contact_info.save()
            return HttpResponse("True")
        except Exception as e:
            print e
            return HttpResponse("False")


class JobInfoView(View):
    def post(self, request):
        try:
            job_info = JobInformation.from_dic(request.POST)
            job_info.save()

            return HttpResponse("True")
        except Exception as e:
            print e
            return HttpResponse("False")


class AssetInfoView(View):
    def post(self, request):
        try:
            asset = AssetInformation.from_dic(request.POST)
            asset.save()
            return HttpResponse("True")

        except Exception as e:
            print e
            return HttpResponse("False")


class BankIncomeView(View):
    @transaction.atomic()
    def post(self, request):
        try:
            maskan_vasighe_type = VasigheType.objects.filter(name='melki').first()
            sanad = None
            if str(maskan_vasighe_type.id) in request.POST.getlist('vasighe_types'):
                sanad = SanadMelkiInformation.from_dic(request.POST)
                sanad.save()
            bank_income = BankIncomeInformation.from_dic(request.POST, sanad)
            bank_income.save()
            SanadMelkiInformation.objects.exclude(bankincomeinformation__in=BankIncomeInformation.objects.all()).delete()
            return HttpResponse("True")

        except Exception as e:
            print e
            return HttpResponse("False")
