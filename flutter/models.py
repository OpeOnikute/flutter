from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm

class Info(models.Model):
	verify = (
		('Voice', 'Voice'),
		('SMS', 'SMS'))

	country_codes = (
		('NG', 'Nigeria'),
		)	
	name = models.CharField(blank=True, null=True,
                                    max_length=30)
	bvn = models.DecimalField(blank=True, null=True, 
		max_digits=11, decimal_places=0)

	verifyUsing = models.CharField(blank=True, null=True, max_length=30,
						choices=verify)

	country = models.CharField(blank=True, null=True, max_length=30,
						choices=country_codes)

	transactionReference = models.CharField(blank=True, null=True,
                                    max_length=30)
	def __unicode__(self):
		return self.name

class Infoform(ModelForm):
    class Meta:
        model = Info
        fields = ['name', 'bvn', 'verifyUsing', 'country']
