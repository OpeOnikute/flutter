from __future__ import unicode_literals
from django.db import models


class Info(models.Model):

    verify = (
        ('Voice', 'Voice'),
        ('SMS', 'SMS')
    )

    country_codes = (
        ('NG', 'Nigeria'),
    )

    name = models.CharField(blank=True, null=True, max_length=30)
    bvn = models.DecimalField(blank=True, null=True, max_digits=11, decimal_places=0)
    verifyUsing = models.CharField(blank=True, null=True, max_length=30, choices=verify)
    country = models.CharField(blank=True, null=True, max_length=30, choices=country_codes)
    transactionReference = models.CharField(blank=True, null=True, max_length=30)

    def __unicode__(self):
        return self.name


class ErrorLogModel(models.Model):
    """
    Logs all errors.
    """

    error_message = models.CharField(max_length=100, null=False, blank=False)
    calling_function = models.CharField(max_length=100, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return str(self.date_added) + ' ' + str(self.error_message) + ' - Function:' + str(self.calling_function)
