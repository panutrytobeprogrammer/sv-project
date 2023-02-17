from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Recentplan, location, Appoint_default
from django.urls import reverse
import datetime
from .program_func import *

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

def add_recent_record(og_name, ds_name):
    og_pos = location.objects.get(name=og_name)
    ds_pos = location.objects.get(name=ds_name)
    plan = Recentplan(user_id=123, origin_name=og_name, origin_pos=og_pos, destin_name=ds_name, destin_pos=ds_pos, timestamp=str(datetime.datetime.now()))
    plan.save()

def planning(request):
    # load template
    template = loader.get_template('planning.html')
    origin_name = request.POST['origin_plan']
    destin_name = request.POST['destination_plan']
    origin_s = s_name(origin_name)
    destin_s = s_name(destin_name)

    # query time
    now = datetime.datetime.now()
    time = query_time(route=f'{origin_s}_{destin_s}', dt=now)
    time = round(float(time))
    now = now.time()

    # get appointment time
    default_time = Appoint_default.objects.all().values()

    context = {
        'origin_name':origin_name,
        'destin_name':destin_name,
        'time':time,
        'now':now,
        'default_time':default_time
    }
    # add_recent_record(origin_name, destin_name)
    return HttpResponse(template.render(context, request))

def visualize(request):
    impt_percent = request.POST['appointment']
    template = loader.get_template('visualize.html')
    return HttpResponse(template.render())

def recent_plan_seeall(request):
    template = loader.get_template('recent.html')
    data = Recentplan.objects.all().order_by('-id')
    context = {
        'recent_data': data
    }
    return HttpResponse(template.render(context, request))

def soon(request):
    template = loader.get_template('comingsoon.html')
    return HttpResponse(template.render())
