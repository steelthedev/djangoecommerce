from django import template
from istore.models import Order,Profile
from django.contrib.auth.models import User
from django.template import RequestContext

register = template.Library()

@register.filter
def cart_count(user):
  if user.is_authenticated:
    query=Order.objects.filter(user=user,complete=False)
    if query.exists():
      return query[0].products.count()
  return 0
