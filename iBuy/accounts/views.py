from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import *
from istore.models import Profile
# Create your views here.
def signup_view(request):
  submitbutton=request.POST.get("submit")

  if request.method=="POST":
    
    form=SignupForm(request.POST)
    if form.is_valid():
      user=form.save()
      user.refresh_from_db()
      user.profile.first_name=form.cleaned_data.get('first_name')
      user.profile.last_name=form.cleaned_data.get('last_name')
      user.profile.email=form.cleaned_data.get('email')
      user.save()
      login(request,user)
      return redirect('istore:homepage')
    
      
    
    
  else:
    form=SignupForm()
  return render(request,'accounts/signup.html',{'form':form})
  
def login_view(request):
  if request.method == "POST":
    form=LoginForm(data=request.POST)
    if form.is_valid():
      user=form.get_user()
      login(request,user)
      if 'next' in request.POST:
        return redirect(request.POST.get('next'))
      else:
        return redirect('istore:homepage')
  
  else:
    form=LoginForm()
  return render(request,'accounts/login.html',{'form':form})
  
  
def logout_view(request):
  if request.method== "POST":
    logout(request)
    return redirect('istore:homepage')
  
  
