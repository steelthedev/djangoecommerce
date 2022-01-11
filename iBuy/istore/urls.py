from django.urls import path
from . import views


app_name='istore'


urlpatterns=[
  path('',views.homepage,name="homepage"),
  path('istore/cart/summary',views.cart_view,name="summary"),
  path('istore/cart/checkout/',views.checkout_view,name="checkout"),
  path('istore/cart/<slug:slug>',views.add_to_cart,name="cart"),
  path('istore/cart_add/<slug:slug>',views.add_one_cart,name="one_cart"),
  path('istore/cart/remove_cart/<slug:slug>',views.remove_cart,name='remove_cart'),
  path('istore/cart/remove_one_cart/<slug:slug>',views.remove_one_cart,name="remove_one_cart"),
  path('istore/product/description/<slug:slug>',views.desc_view,name="description"),
  path('istore/cart/verify_payment/<str:ref>', views.verify_payment, name="verify_payment"),
  
  
  ]