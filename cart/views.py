from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import Context, loader
from items.models import Store, Item
import json

def cart(request):
    template = loader.get_template('cart.html')
    context = Context({})
    return HttpResponse(template.render(context))
