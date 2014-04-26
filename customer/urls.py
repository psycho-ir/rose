from django.conf.urls import patterns, url
from customer.views import *


urlpatterns = patterns('',
                       url(r'^customer_info', CustomerInfoView.as_view(), name='customer_info'),
                       url(r'^contact_info', ContactInfoView.as_view(), name='contact_info'),
                       url(r'^job_info', JobInfoView.as_view(), name='job_info'),
                       url(r'^asset_info', AssetInfoView.as_view(), name='asset_info'),
                       url(r'^bank_income_info', BankIncomeView.as_view(), name='bank_income_info'),
)