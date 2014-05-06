from django.db import models
from customer.models.common import Customer
from rose_config.models import VasigheType


class Guarantor(models.Model):
    customer = models.ForeignKey(Customer)
    vasighe_type = models.ForeignKey(VasigheType)

