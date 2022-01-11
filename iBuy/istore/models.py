from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Sum
from django.dispatch import receiver
from django.shortcuts import reverse
from .paystack import PayStack
# Create your models here.
#class Customer(models.Model):
  #User=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
  #name=models.CharField(max_length=200,null=True)
  #Email=models.EmailField(max_length=200)
  
  #def __str__(self):
   # return self.name
   

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)


    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Categories(models.Model):
  category=models.CharField(max_length=500,null=False)
  date_added=models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.category




class Product(models.Model):
  name=models.CharField(max_length=200,null=True)
  slug=models.SlugField()
  category=models.ForeignKey(Categories,on_delete=models.SET_NULL,blank=True,null=True)
  price=models.FloatField()
  digital=models.BooleanField(default=False,null=True,blank=False)
  thumb=models.ImageField(default='default.png',null=True)
  description=models.TextField(null=True)
  def __str__(self):
    return self.name
    
  #def get_absolute_url(self):
    #return reverse("istore:cart",kwargs={'slug':self.slug})


  
class ShippingAddress(models.Model):
  customer=models.ForeignKey(Profile,on_delete=models.SET_NULL,blank=True,null=True)
  address=models.CharField(max_length=250)
  city=models.CharField(max_length=250)
  phone_number=models.IntegerField(null=True)
  zip = models.CharField(null=True, max_length=200)
  country = models.CharField(null=True, max_length=200)
  
  def __str__(self):
    return self.address

    
    

class OrderItem(models.Model):
  customer=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
  product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
  quantity=models.IntegerField(default=1,null=True,blank=True)
  complete=models.BooleanField(default=False,null=True,blank=False)
  date_added=models.DateTimeField(auto_now_add=True)

  
  def __str__(self):
    return f"{self.quantity} of {self.product.name}"
  @property
  def get_item_price(self):
    total =self.product.price * self.quantity
    return total





class Order(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
  customer=models.ForeignKey(Profile,on_delete=models.SET_NULL,blank=True,null=True)
  products=models.ManyToManyField(OrderItem)
  address=models.ForeignKey(ShippingAddress,on_delete=models.SET_NULL,null=True)
  date_order=models.DateTimeField(auto_now_add=True)
  amount=models.CharField(null=True,max_length=200)
  complete=models.BooleanField(default=False,null=True,blank=True)
  transaction_id=models.CharField(max_length=100)
  def __str__(self):
    return f'{self.customer}'
  @property
  def get_cart_total(self):
    orderitem=self.products.all()
    total=sum([item.get_item_price for item in orderitem])
    return total
    
  def verify_payment(self):
    paystack = PayStack()
    order_item = OrderItem.objects.filter(customer =self.customer , complete = False)
    status, result = paystack.verify_payment(self.transaction_id , self.get_cart_total)
    if status:
      if result['amount'] / 100 == self.get_cart_total:
        self.complete = True
        self.amount = self.get_cart_total
        self.products.complete = True
        for order_item in order_item:
            order_item.complete = True
            order_item.save()
        self.save()
     

      if self.complete:
          return True
    return False
    
    
class Payment(models.Model):
  customer=models.ForeignKey(Profile,on_delete=models.SET_NULL,blank=True,null=True)
  amount=models.IntegerField(null=True,blank=True)
  date_paid=models.DateTimeField(auto_now_add=True)
  reference=models.CharField(max_length=100)
  
  
  def __str__(self):
    return f'{self.customer}'

  
  

  
  
  
  