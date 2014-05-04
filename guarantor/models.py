from django.db import models
from customer.models import CustomerInformation
from rose_config.models import VasigheType


class Guarantor(models.Model):
    customer = models.ForeignKey(CustomerInformation)
    vasighe_type = models.ForeignKey(VasigheType)

