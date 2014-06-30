from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http.response import HttpResponse
from django.template import loader
from django.template.context import RequestContext
from django.views.generic import View
from core_connection.customer_repository import find_customer
from rose_config.exceptions import ValidationException
from django.utils.translation import ugettext as _
from rose_config.response import generate_error_response, generate_ok_response
from start_grant.models import BankVasigheInformation, SanadMelkiInformation
from customer.models.real_models import *


class RegisterRealCustomerView(View):
    def get(self, request):

        customer_id = request.GET.get('customer_id')
        next_level = request.GET.get('next', None)
        customer = None
        message = None
        if customer_id is not None and customer_id != '':
            try:
                if len(find_customer(customer_id)) == 0:
                    message = 'customer does not exist'
                customer = RealCustomerInformation.objects.get(pk=customer_id)

            except ObjectDoesNotExist as e:
                print e

        provinces = Province.objects.all()
        towns = Town.objects.filter(province_id=provinces.first().id)
        all_towns = Town.objects.all()
        job_types = JobType.objects.all()
        certificate_types = JobCertificateType.objects.filter(type='haghighi')
        context = RequestContext(request, {'customer_type': 'haghighi',
                                           'customer': customer,
                                           'provinces': provinces,
                                           'towns': towns,
                                           'job_types': job_types,
                                           'certificate_types': certificate_types,
                                           'customer_id': customer_id,
                                           'message': message,
                                           'all_towns': all_towns,
                                           'next_level': next_level
        })

        template = loader.get_template('register_customer.html')

        return HttpResponse(template.render(context))


class RegisterEnterpriseCustomerView(View):
    def get(self, request):
        customer_id = request.GET.get('customer_id')
        customer = None
        message = None
        if customer_id is not None and customer_id != '':
            try:
                if len(find_customer(customer_id)) == 0:
                    message = 'customer does not exist'
                customer = RealCustomerInformation.objects.get(pk=customer_id)

            except ObjectDoesNotExist as e:
                print e

        provinces = Province.objects.all()
        towns = Town.objects.filter(province_id=provinces.first().id)
        all_towns = Town.objects.all()
        job_types = JobType.objects.all()
        certificate_types = JobCertificateType.objects.filter(type='haghighi')
        context = RequestContext(request, {'customer_type': 'haghighi',
                                           'customer': customer,
                                           'provinces': provinces,
                                           'towns': towns,
                                           'job_types': job_types,
                                           'certificate_types': certificate_types,
                                           'customer_id': customer_id,
                                           'message': message,
                                           'all_towns': all_towns
        })

        template = loader.get_template('register_enterprise_customer.html')

        return HttpResponse(template.render(context))


class CustomerInfoView(View):
    def post(self, request):
        try:
            customer_info = RealCustomerInformation.from_dic(request.POST)
            customer_info.save()
            return generate_ok_response()

        except ValidationException as e:
            return generate_error_response(e.message)
        except Exception as e:
            print(e)
            return generate_error_response()


class ContactInfoView(View):
    def post(self, request):
        try:
            contact_info = ContactInformation.from_dic(request.POST)
            contact_info.save()
            return generate_ok_response()
        except Exception as e:
            print e
            return generate_error_response()


class JobInfoView(View):
    def post(self, request):
        try:
            job_info = JobInformation.from_dic(request.POST)
            job_info.save()

            return generate_ok_response()
        except Exception as e:
            print e
            return generate_error_response()


class AssetInfoView(View):
    def post(self, request):
        try:
            asset = AssetInformation.from_dic(request.POST)
            asset.save()
            return generate_ok_response()

        except Exception as e:
            print e
            return generate_error_response()


class BankIncomeView(View):
    @transaction.atomic()
    def post(self, request):
        try:
            no_vasighe = request.POST.get('no_vasighe_info')
            no_income = request.POST.get('no_income')

            # when we don't  want to save income
            # todo here we have a bad design and we need to change this block of code
            if not no_income:
                bank_income = BankIncomeInformation.from_dic(request.POST)
                bank_income.save()

            if not no_vasighe:
                vasighes = request.POST.getlist('vasighe_types')
                if len(vasighes) == 0:
                    print "There is no selected vasighe_type"
                    return generate_error_response("There is no selected vasighe_type")

                banks = request.POST.getlist('banks')

                if len(banks) == 0:
                    print "There is no selected bank"
                    return generate_error_response("There is no selected bank")

                maskan_vasighe_type = VasigheType.objects.filter(name='melk-tejari-edari').first()
                sanad = None
                if str(maskan_vasighe_type.id) in vasighes:
                    sanad = SanadMelkiInformation.from_dic(request.POST)
                    sanad.save()
                bank_vasighe = BankVasigheInformation.from_dic(request.POST, sanad)
                bank_vasighe.save()
                SanadMelkiInformation.objects.exclude(
                    bankvasigheinformation__in=BankVasigheInformation.objects.all()).delete()

            return generate_ok_response()

        except Exception as e:
            print e
            return generate_error_response()
