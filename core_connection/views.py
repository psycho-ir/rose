from django.http.response import HttpResponse
from django.shortcuts import render
from customer_repository import *
from deposit_repository import *


def create_check_response(object):
    if len(object) == 0:
        return HttpResponse(False)
    else:
        return HttpResponse(True)


def is_customer_valid(request, customer_id):
    customer = find_customer(customer_id)
    return create_check_response(customer)


def is_deposit_valid(request, customer_id, deposit_number_1, deposit_number_2):
    deposit = find_deposit(customer_id, deposit_number_1 + '.' + deposit_number_2)
    return create_check_response(deposit)

