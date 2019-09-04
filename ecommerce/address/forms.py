from django import forms

from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields=[
          # 'billing_profile',
          # 'addressType',
           'addressline1',
           'addressline2',
           'city',
           'state',
           'country',
           'postalcode',
        ]
