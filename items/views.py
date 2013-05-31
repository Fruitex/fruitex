from django.http import HttpResponse
from django.template import Context, loader
from items.models import Store, Item

def itemlist(request):
    template = loader.get_template('itemlist.html')
    context = Context({'itemList' : Item.objects.all()[:4]})
    return HttpResponse(template.render(context))
