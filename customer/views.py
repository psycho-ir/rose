from django.db import transaction
from django.http.response import HttpResponse
from django.views.generic import View
from customer.models import RealCustomerInformation, ContactInformation, JobInformation, BankIncomeInformation,  AssetInformation
from rose_config.models import VasigheType
from start_grant.models import BankVasigheInformation, SanadMelkiInformation


class CustomerInfoView(View):
    def post(self, request):
        try:
            customer_info = RealCustomerInformation.from_dic(request.POST)
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
            no_vasighe = request.POST.get('no_vasighe_info')
            bank_income = BankIncomeInformation.from_dic(request.POST)
            bank_income.save()
            if not no_vasighe:
                vasighes = request.POST.getlist('vasighe_types')
                if len(vasighes) == 0:
                    print "There is no selected vasighe_type"
                    return HttpResponse("False")

                banks = request.POST.getlist('banks')

                if len(banks) == 0:
                    print "There is no selected bank"
                    return HttpResponse("False")

                maskan_vasighe_type = VasigheType.objects.filter(name='melki').first()
                sanad = None
                if str(maskan_vasighe_type.id) in vasighes:
                    sanad = SanadMelkiInformation.from_dic(request.POST)
                    sanad.save()
                bank_vasighe = BankVasigheInformation.from_dic(request.POST, sanad)
                bank_vasighe.save()
                SanadMelkiInformation.objects.exclude(
                    bankvasigheinformation__in=BankVasigheInformation.objects.all()).delete()

            return HttpResponse("True")

        except Exception as e:
            print e
            return HttpResponse("False")
