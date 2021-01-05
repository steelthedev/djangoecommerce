
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from istore.models import Profile

class SignupForm(UserCreationForm):
  username=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
  first_name=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
  last_name=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
  email=forms.EmailField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
  password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),required=True,label='Password')
  
  password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),required=True,label='Repeat Password')
  
  class Meta:
    model=User
    
    
    fields=[
      'username','first_name','last_name','email','password1','password2'
      ]


class LoginForm(AuthenticationForm):
   username=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
   
   password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),required=True,label='Password')
   
   class Meta:
     model=User
     
     fields=['username','password']
   
   
    
    