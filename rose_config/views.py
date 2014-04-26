from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from rose_config.models import Town


class TownView(View):
    def get(self, request, province_id):
        towns = Town.objects.filter(province_id=province_id)
        encoded = serializers.serialize('json', towns)
        return HttpResponse(encoded)
