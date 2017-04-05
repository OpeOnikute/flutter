from django import forms


class InfoForm(forms.Form):

    verify = (
        ('Voice', 'Voice'),
        ('SMS', 'SMS'))

    country_codes = (
        ('NG', 'Nigeria'),
        )   
    
    name = forms.CharField(max_length=30)
    bvn = forms.DecimalField(max_digits=11)

    verifyUsing = forms.CharField(max_length=30, widget=forms.Select(choices=verify))

    country = forms.CharField(widget=forms.Select(choices=country_codes))
