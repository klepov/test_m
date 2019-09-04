import datetime

from django.db import models
from django.contrib.auth.models import User as A_User
from django.db.models import Count, Sum


class Item(models.Model):
    dttm_created = models.DateTimeField(default=datetime.datetime.now)
    dttm_deleted = models.DateTimeField(default=datetime.datetime.now)

    name = models.CharField(max_length=255)
    price = models.FloatField()


class BoughtUsersManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            bought_items_count=Count('bought_items')).annotate(total_sum=Sum('bought_items__price'))


class User(A_User):
    dttm_created = models.DateTimeField(default=datetime.datetime.now)
    dttm_deleted = models.DateTimeField(default=datetime.datetime.now)

    SEX_FEMALE = 'F'
    SEX_MALE = 'M'
    SEX_CHOICES = (
        (SEX_FEMALE, 'Female',),
        (SEX_MALE, 'Male',),
    )

    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    bought_items = models.ManyToManyField(Item)
    objects = models.Manager()
    bought_users = BoughtUsersManager()
