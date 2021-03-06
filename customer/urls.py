from django.conf.urls import patterns, url
from customer.enterprise_views import *
from customer.views import *


urlpatterns = patterns('',
                       url(r'^real_register', RegisterRealCustomerView.as_view(), name='real_register'),
                       url(r'^enterprise_register', RegisterEnterpriseCustomerView.as_view(),
                           name='enterprise_register'),
                       url(r'^customer_info', CustomerInfoView.as_view(), name='customer_info'),
                       url(r'^contact_info', ContactInfoView.as_view(), name='contact_info'),
                       url(r'^job_info', JobInfoView.as_view(), name='job_info'),
                       url(r'^asset_info', AssetInfoView.as_view(), name='asset_info'),
                       url(r'^bank_income_info', BankIncomeView.as_view(), name='bank_income_info'),

                       url(r'^enterprise_customer_info', EnterpriseCustomerInfoView.as_view(),
                           name='enterprise_customer_info'),

                       url(r'^enterprise_contact_info', EnterpriseContactInformationView.as_view(),
                           name='enterprise_contact_info'),
                       url(r'^enterprise_activity_info', EnterpriseActivityView.as_view(),
                           name='enterprise_activity_info'),
                       url(r'^enterprise_activity_list', EnterpriseActivityListView.as_view(),
                           name='enterprise_activity_list'),
                       url(r'^enterprise_activity_delete', EnterpriseActivityDeleteView.as_view(),
                           name='enterprise_activity_delete'),
                       url(r'^board_of_director', BoardOfDirectorView.as_view(), name='board_of_director'),
                       url(r'^director_list', BoardOfDirectorListView.as_view(), name='director_list'),
                       url(r'^enterprise_asset_info', EnterpriseAssetInfoView.as_view(), name='enterprise_asset_info'),
)