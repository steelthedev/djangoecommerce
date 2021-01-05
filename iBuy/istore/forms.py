from django import forms
from .models import *




class ShipAddress(forms.ModelForm):
  
  
  address=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
  
  
  city=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
  
  
  phone_number=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
  class Meta:
    model=ShippingAddress
    
    fields=[
      
      'address','city','phone_number'
      
      ]