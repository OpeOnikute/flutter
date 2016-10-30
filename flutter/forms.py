from django import forms

from .models import Info

class InfoForm(forms.ModelForm):
	
	class Meta:
		model = Info
		# name = forms.CharField()
		# bvn = forms.DecimalField()
		# verifyUsing = forms.CharField()
		# country = forms.CharField()
		fields = ('name', 'bvn', 'verifyUsing', 'country')
		widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'bvn': forms.NumberInput(attrs={'placeholder': 'Enter 11-digit BVN'}),
  #           'verifyUsing': forms.Select(),
  #           'country': forms.Select(),

        }

		def save(self, commit=False):
	            user = super(InfoForm, self).save(commit=False)
	            if commit:
	                user.save()
	            return user
