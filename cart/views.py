from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt
from cart.models import Order
import json

def cart(request):
    template = loader.get_template('cart.html')
    context = Context({})
    return HttpResponse(template.render(context))

@csrf_exempt
def checkout(request):
  if request.method == 'POST':
    name = request.POST['name']
    phone = request.POST['phone']
    address = request.POST['address']
    postcode = request.POST['postcode']
    ids = request.POST['ids']
    price = float(request.POST['price'])
    tax = float(request.POST['tax'])
    shipping = float(request.POST['shipping'])
    Order(name=name, address=address, phone=phone, postcode=postcode,
        items=ids, price=price, tax=tax, shipping=shipping, status='pending').save()
    return HttpResponse('success')
  else:
    return HttpResponse('error')
