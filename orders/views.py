from django.http import HttpResponse
from django.template import Context, loader
from home.models import Store, Item
from django.shortcuts import redirect
from fruitex.views import error

