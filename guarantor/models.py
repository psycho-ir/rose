from django.db import models
from customer.models import CustomerInformation


class Guarantor(models.Model):
    customer = models.ForeignKey(CustomerInformation)

