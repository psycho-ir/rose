from django.db import models
from customer.models import RealCustomerInformation, Customer
from rose_config.models import VasigheType


class Guarantor(models.Model):
    customer = models.ForeignKey(Customer)
    vasighe_type = models.ForeignKey(VasigheType)

