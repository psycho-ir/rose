__author__ = 'soroosh'

from django.db import models

CUSTOMER_TYPE = (
    ("haghighi", "haghighi"),
    ("hoghooghi", "haghighi"),
)


class Customer(models.Model):
    class Meta:
        app_label = 'customer'

    type = models.CharField(choices=CUSTOMER_TYPE, max_length=30)
    customer_code = models.CharField(max_length=10, primary_key=True)
