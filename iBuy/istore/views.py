from django.shortcuts import render,redirect
from  .models import *
from django.shortcuts import get_object_or_404
from random import randint
from django.contrib import messages
from django.contrib.auth.decorators  import login_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import ShipAddress
from django.http.request import HttpRequest
from django.http.response import HttpResponse


# Create your views here.

def homepage(request):
 
  product=Product.objects.all()
  try:
    user=request.user
    customer=request.user.profile
    order=Order.objects.get(customer=customer,user=user,complete=False)
    context={
      'product':product,
      'order':order
    }
  except:
    context={
      'product':product,
    }
    return render(request,'istore/index.html', context)

  return render(request,'istore/index.html',context)


def desc_view(request,slug):
  product=Product.objects.get(slug=slug)
  context = {
    'product':product
    }
  return render(request,'istore/product-single.html',context)

@login_required
def add_to_cart(request,slug):
  if request.user.is_authenticated:
    user=request.user
    customer=request.user.profile
    product=get_object_or_404(Product, slug=slug)
    order_item, created=OrderItem.objects.get_or_create(customer=customer,product=product,complete=False)
    order_qs=Order.objects.filter(customer=customer,user=user,complete=False)
    if order_qs.exists():
      order=order_qs[0]
      if order.products.filter(product__slug=product.slug).exists():
        
        order_item.quantity += 1
        order_item.save()
        messages.info(request,"Quantity successfully updated")
        return redirect('istore:homepage')
      else:
      
        order.products.add(order_item)
        messages.info(request,"item successfully added to cart")
        return redirect('istore:homepage')
    else:
      random=randint(1000,70000)
      order=Order.objects.create(customer=customer,user=user,transaction_id=random,complete=False)
      order.products.add(order_item)
      messages.info(request,"Cart successfully created and item added")
      return redirect('istore:description',slug=slug)
  else:
    messages.info(request,"You must be logged in")
    return redirect('istore:homepage')
  
  #return render(request,'istore/cart.html')
  
@login_required
def remove_cart(request,slug):
  if request.user.is_authenticated:
    customer=request.user.profile
    product=get_object_or_404(Product, slug=slug)
    order_qs=Order.objects.filter(customer=customer,complete=False)
    if order_qs.exists():
      order=order_qs[0]
      if order.products.filter(product__slug=product.slug).exists():
        order_item=OrderItem.objects.filter(product=product,customer=customer,complete=False)[0]
        order.products.remove(order_item)
        order_item.delete()
        messages.info(request,"item removed from cart")
        return redirect('istore:summary')
      else:
        messages.info(request,"item not in cart")
        return redirect('istore:homepage')
    else:
      messages.info(request,"no active order")
      return redirect('istore:homepage')
  else:
    messages.info(request,"You must login first")
    return redirect('istore:homepage')
    
    
    
@login_required
def cart_view(request):
  user=request.user
  customer=request.user.profile
  try:
    order=Order.objects.get(customer=customer,user=user,complete=False)
    return render(request,'istore/cart.html',{'order':order})
  except ObjectDoesNotExist:
    messages.error(request,"No active Order")
    return redirect('/')

def remove_one_cart(request,slug):
  if request.user.is_authenticated:
    user=request.user
    customer=request.user.profile
    product=get_object_or_404(Product, slug=slug)
    order_item=OrderItem.objects.get(product=product,customer=customer,complete=False)
    order_qs=Order.objects.filter(customer=customer,complete=False)
    if order_qs.exists():
      order=order_qs[0]
      if order.products.filter(product__slug=product.slug).exists():
        
        if order_item.quantity > 1:
          order_item.quantity -=1
          order_item.save()
        else:
          order.products.remove(order_item)
          order_item.save()
        messages.info(request,"Quantity  successfully updated")
        return redirect('istore:summary')
      
  else:
    messages.info(request,"You must be logged in")
    return redirect('istore:homepage')


def add_one_cart(request,slug):
  if request.user.is_authenticated:
    user=request.user
    customer=request.user.profile
    product=get_object_or_404(Product, slug=slug)
    order_item, created=OrderItem.objects.get_or_create(customer=customer,product=product,complete=False)
    order_qs=Order.objects.filter(customer=customer,user=user,complete=False)
    if order_qs.exists():
      order=order_qs[0]
      if order.products.filter(product__slug=product.slug).exists():
        
        order_item.quantity += 1
        order_item.save()
        messages.info(request,"Quantity successfully updated")
        return redirect('istore:summary')
    
    
def checkout_view(request):
  context ={}
  submitbutton = request.POST.get("btn-s")
  paystack_public = "pk_test_ef1bea703713ac519754d7b88f3b56ea141c1d67"
  try:
    order=Order.objects.get(customer=request.user.profile,complete=False)
  except ObjectDoesNotExist:
    return redirect("/")

  if request.method == 'POST':
    customer=request.user.profile
    address = request.POST['address']
    city = request.POST['city']
    phone_number = request.POST['phone_number']
    zip = request.POST['zip']
    country = request.POST['country']
    try:
      order=Order.objects.get(customer=customer,complete=False)  
      ship_address=ShippingAddress(customer=customer,
      city=city,
      address=address,
      phone_number=phone_number, zip=zip, country = country)
      ship_address.save()
      paystack_secret = "sk_test_b1630e59eb70f2592023210935c7894455b9ac1b"
      order.address=ship_address
      order.save()
      messages.success(request,"Success")
    except ObjectDoesNotExist:
      messages.error(request,"No active Order")
      return redirect('/')
  context={
    'order':order,
    'submitbutton':submitbutton,
    'paystack_public':paystack_public,
    'order':order
    }
  return render(request,'istore/checkout.html',context)
    
def shipping_address(request):
  return redirect('istore:checkout_view')
  

def verify_payment(request:HttpRequest, ref) -> HttpResponse:
    order = get_object_or_404(Order, transaction_id=ref)
    verified = order.verify_payment()
    if verified:
        messages.success(request," Alright mate you have successfullly purchased our package")
    else:
        messages.error(request,"verification failed ")
    return redirect('istore:checkout')
