from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Recentplan, location
from django.urls import reverse

# Create your views here.

def index(request):
    # load template
    template = loader.get_template('home.html')
    # get recent data
    data_recent = Recentplan.objects.last()
    location_data = location.objects.all().values()
    context = {
        'last_data': data_recent,
        'location_data': location_data
    }
    return HttpResponse(template.render(context, request))

def map_home(request):
    template = loader.get_template('map.html')
    return HttpResponse(template.render())

def addrecord(request, id):
    location_id = request.POST['loc_id'] # fix
    name = request.POST['loc_name']
    locate = loader(location_id=location_id, name=name)
    locate.save()
    # return HttpResponseRedirect(reverse('index'))

def recent_plan_seeall(request):
    template = loader.get_template('recent.html')
    data = Recentplan.objects.all().values()
    context = {
        'recent_data': data
    }
    return HttpResponse(template.render(context, request))

def soon(request):
    template = loader.get_template('comingsoon.html')
    return HttpResponse(template.render())
