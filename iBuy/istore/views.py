from django.shortcuts import render,redirect
from  .models import *
from django.shortcuts import get_object_or_404
from random import randint
from django.contrib import messages
from django.contrib.auth.decorators  import login_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import ShipAddress
from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction
from python_paystack.objects.transactions import Transaction
from python_paystack.managers import TransactionsManager
from python_paystack.paystack_config import PaystackConfig

# Create your views here.

def homepage(request):
  product=Product.objects.all()
  return render(request,'istore/homepage.html',{'product':product})


def desc_view(request,slug):
  product=Product.objects.get(slug=slug)
  return render(request,'istore/desc.html',{'product':product})

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
        messages.info(request,"Quantity  successfully updated")
        return redirect('istore:summary')
      else:
      
        order.products.add(order_item)
        messages.info(request,"item successfully added to cart")
        return redirect('istore:description',slug=slug)
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
    
    
    
def checkout_view(request):
  submitbutton = request.POST.get("submit")
  order=Order.objects.get(customer=request.user.profile,complete=False)
  if request.method == 'POST':
    customer=request.user.profile
    form=ShipAddress(request.POST)
    
    try:
      order=Order.objects.get(customer=customer,complete=False)
      if form.is_valid():
        city=form.cleaned_data.get('city')
        address=form.cleaned_data.get('address')
        phone_number=form.cleaned_data.get('phone_number')
        ship_address=ShippingAddress(customer=customer,
        city=city,
        address=address,
        phone_number=phone_number)
        ship_address.save()
        
        order.address=ship_address
        
        order.save()
        messages.success(request,"Success")
        #return redirect('istore:checkout')
      else:
        messages.error(request,"Failed")
    except ObjectDoesNotExist:
      messages.error(request,"No active Order")
      return redirect('/')
    
      
  
  else:
    form=ShipAddress()
  return render(request,'istore/checkout.html',{'form':form, 'order':order,'submitbutton':submitbutton})
    
def shipping_address(request):
  return redirect('istore:checkout_view')
  
"""def payment_view(request):
  if request.user.is_authenticated:
    customer=request.user.profile
    order=Order.objects.get(customer=customer,complete=False)
    payment=Payment
    try:
      order=Order.objects.get(customer=customer,complete=False)
      payment.objects.create(
        customer=customer,
        amount=order.get_cart_total,
        reference=order.transaction_id
        )
      order.amount=payment.amount
      order.complete=True
      order.save()
      messages.success(request,"it do")
      return redirect('istore:checkout')
    except ObjectDoesNotExist:
      messages.error(request,"Error")
      return redirect('istore:checkout')"""
      
def payment_view(request):
  customer=request.user.profile
  order=Order.objects.get(customer=customer,complete=False)
  #response = Transaction.initialize(reference='555555555',amount=order.get_cart_total,emai='request.user.profile.email')
  #return response


  transaction = Transaction(2000, 'akinwumikaliyanu@gmail.com')
  transaction_manager = TransactionsManager()
  transaction = transaction_manager.initialize_transaction('STANDARD', transaction)
  #Starts a standard transaction and returns a transaction object
  
  transaction.authorization_url
  #Gives the authorization_url for the transaction
  
  #Transactions can easily be verified like so
  transaction = transaction_manager.verify_transaction(transaction)