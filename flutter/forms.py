from django import forms

from .models import Info

# class InfoForm(forms.ModelForm):
    
#     class Meta:
#         model = Info
#         # name = forms.CharField()
#         # bvn = forms.DecimalField()
#         # verifyUsing = forms.CharField()
#         # country = forms.CharField()
#         fields = ('name', 'bvn', 'verifyUsing', 'country')
#         widgets = {
#         'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
#         'bvn': forms.NumberInput(attrs={'placeholder': 'Enter 11-digit BVN'}),
#   #           'verifyUsing': forms.Select(),
#   #           'country': forms.Select(),
#         }

#         def save(self, commit=False):
#             user = super(InfoForm, self).save(commit=False)
#             if commit:
#                 user.save()
#             return user

class InfoForm(forms.Form):
    verify = (
        ('Voice', 'Voice'),
        ('SMS', 'SMS'))

    country_codes = (
        ('NG', 'Nigeria'),
        )   
    
    name = forms.CharField( max_length=30)
    bvn = forms.DecimalField(  max_digits=11)

    verifyUsing = forms.CharField( max_length=30,
                    widget=forms.Select(choices=verify),
)

    country = forms.CharField(
                        widget=forms.Select(choices=country_codes))

    





    # def as_myp(self):
    #     "Returns this form rendered as HTML <p>s."
    #     return self._html_output(
    #         normal_row = '<p%(html_class_attr)s>%(label)s</p> <p>%(field)s%(help_text)s</p>',
    #         error_row = '%s',
    #         row_ender = '</p>',
    #         help_text_html = ' <span class="helptext">%s</span>',
    #         errors_on_separate_row = True)    

        
