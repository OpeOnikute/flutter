from __future__ import unicode_literals

from django.db import models

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

	def __unicode__(self):
		return self.name

