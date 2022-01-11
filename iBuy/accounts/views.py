from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import *
from istore.models import Profile
from django.contrib.auth.hashers import make_password
# Create your views here.
def signup_view(request):
  if request.method=="POST":
    username = request.POST['username']
    email = request.POST['email']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    password1 = request.POST['password']
    password2 = request.POST['password2']

    if username and email and first_name and last_name and password1 and password2:
      if password1 == password2:
        if '@' in email:
          if len(password1) > 4:
            if User.objects.filter(username = username).exists():
              messages.info(request, " User Exists Already")
              return redirect("accounts:signup")
            else:
              password_hashed = make_password(password1)
              User.objects.create(username = username, first_name = first_name, last_name = last_name, email=email, password = password_hashed )
              messages.info(request, "User Created succesfully, Login")
              return redirect('accounts:login')
          else:
            messages.info(request, " Password must be greater than 4 characters ")
            return redirect("accounts:signup")
        else:
          messages.info(request, " Input a valid email")
          return redirect("accounts:signup")
      else:
        messages.info(request, " Passwords do not match")
        return redirect("accounts:signup")
    else:
      None

  return render(request,'accounts/signup.html')
  
def login_view(request):
  if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        if User.objects.filter(username=username):
            user = authenticate(request,username = username , password = password)

            if user is not None:
                login(request, user)
                return redirect("istore:homepage")

            else:
                messages.info(request, "Incorrect Details" )
                return redirect("accounts:login")

        else:
            messages.info(request, "This User Does Not Exist" )
            return redirect("accounts:login")
  return render(request, 'accounts/login.html')

  
  
def logout_view(request):
  logout(request)
  return redirect('istore:homepage')
  
  
