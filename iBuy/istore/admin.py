from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ShippingAddress)
admin.site.register(Categories)
admin.site.register(OrderItem)
admin.site.register(Payment)
