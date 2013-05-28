from django.http import HttpResponse
from django.template import Context, loader
from items.models import Store, Item

def index(request):
    template = loader.get_template('home/index.html')
    context = Context({})
    return HttpResponse(template.render(context))