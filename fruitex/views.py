from django.http import HttpResponse
from django.template import Context, loader
from home.models import Store, Item
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from cart.models import Order

def home(request):
    template = loader.get_template('index.html')
    context = Context({})
    return HttpResponse(template.render(context))

@csrf_exempt
def redir(request):
    return redirect('/%s' % request.GET['to'])

@csrf_exempt
def checkout_return(request):
    invoice=request.GET['invoice']
    return render_to_response("checkout_return.html", {'invoice' : invoice})

@csrf_exempt
def check_order(request):
    if 'invoice' in request.GET:
      invoice = request.GET['invoice']
    else:
      invoice = ''
    orders = []
    for o in Order.objects.filter(invoice=invoice):
        orders.append(o)
    if len(orders) == 0:
        return render_to_response("error.html", {})
    else:
        return render_to_response("check_order.html", {'order' : orders[0]})


def fruitex_admin(request):
    from cart.models import Order
    orders = []
    for o in Order.objects.filter(status='paid'):
       orders.append(o)
    return render_to_response("fruitex_admin.html", {'orders' : orders})
  
