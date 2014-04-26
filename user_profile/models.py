from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

#It is a template for different commisions
# like : Degree1 , Degree2, Momtaz, ....

class Role(models.Model):
    class Meta:
        db_table = "p_role"

    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=100)


class Substitution(models.Model):
    class Meta:
        db_table = "p_substitute"

    main_role = models.ForeignKey(Role, related_name='main_substitution_set')
    substitution_role = models.ForeignKey(Role, related_name='substitution_substitution_set')


class CommissionDefinition(models.Model):
    class Meta:
        db_table = "p_comm_definition"

    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=100)
    roles = models.ManyToManyField(to=Role, related_name='commission_definitions')
    substitutions = models.ManyToManyField(Substitution, related_name='commission_definitions')
    number_of_commision = models.IntegerField(default=2)
    max_aghsati_amount = models.BigIntegerField(default=100000)
    max_yek_ja_amount = models.BigIntegerField(default=100000)
    max_aghsati_duration = models.IntegerField(default=12)
    max_yek_ja_duration = models.IntegerField(default=8)


class UserProfile(models.Model):
    class Meta:
        db_table = "p_user_profile"

    user = models.OneToOneField(User, related_name='profile')
    branch_code = models.IntegerField(default=0)
    role = models.ForeignKey(Role, default=1)


class Commission(models.Model):
    class Meta:
        db_table = "p_comm"

    definition = models.ForeignKey(CommissionDefinition, related_name='commissions')
    members = models.ManyToManyField(UserProfile)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)








