from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Recentplan, location, Appoint_default, planning_to_visualize, Planning_temp
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

def add_recent_record(og_name, ds_name, avg_time, plantime):
    og_pos = location.objects.get(name=og_name)
    ds_pos = location.objects.get(name=ds_name)
    plan = Recentplan(user_id=123, origin_name=og_name, origin_pos=og_pos, destin_name=ds_name, destin_pos=ds_pos, avg_time=avg_time, timestamp=str(plantime))
    plan.save()

def planning(request):
    # load template
    template = loader.get_template('planning.html')
    origin_name = request.POST['origin_plan']
    destin_name = request.POST['destination_plan']
    plantime = request.POST['plantime']
    origin_s = s_name(origin_name)
    destin_s = s_name(destin_name)

    # query time
    plantime = pd.to_datetime(plantime)
    time = query_time(route=f'{origin_s}_{destin_s}', dt=plantime)
    ff_time = time['ff_time']
    avg_time = time['avg_time']
    p95_time = time['p95_time']

    dep_time_ff = plantime - datetime.timedelta(minutes=ff_time)
    dep_time_avg = plantime - datetime.timedelta(minutes=avg_time)
    dep_time_p95 = plantime - datetime.timedelta(minutes=p95_time)

    # get appointment time
    # default_time = Appoint_default.objects.all().values()

    # save to planning temp table
    Planning_temp(plantype='Fasten', og=origin_name, start=dep_time_ff, ds=destin_name, arrv=plantime, traveltime=ff_time).save()
    Planning_temp(plantype='Most popular', og=origin_name, start=dep_time_avg, ds=destin_name, arrv=plantime, traveltime=avg_time).save()
    Planning_temp(plantype='Suggested', og=origin_name, start=dep_time_p95, ds=destin_name, arrv=plantime, traveltime=p95_time).save()
    
    dep_time = Planning_temp.objects.all().order_by('-id')

    context = {
        'origin_name':origin_name,
        'destin_name':destin_name,
        'time':time,
        'now':plantime.strftime('%H:%M'),
        # 'default_time':default_time,
        'dep_time_ff':dep_time_ff.strftime('%H:%M'),
        'dep_time_avg':dep_time_avg.strftime('%H:%M'),
        'dep_time_p95':dep_time_p95.strftime('%H:%M'),
        'dep_time': dep_time
    }
    return HttpResponse(template.render(context, request))

def visualize(request, plantype):
    # impt_percent = request.POST['percentage']
    template = loader.get_template('visualize.html')
    # # plan_time = query_time()[1]
    # # df = query_visual_tti('monday', '8:00:00')

    # lastplan = Recentplan.objects.last()

    # # test plt show
    # filename = f'{datetime.datetime.now()}'
    # pie_chart(30, 65, filename)
    # # pie_img_path = f'home/chart_img/pie_({filename}).png'
    # # bar_chart_path = 'pathofbarchart'
    # # data = planning_to_visualize(origin_name=lastplan.origin_name, destin_name=lastplan.destin_name, avg_time=lastplan.avg_time, percent=impt_percent, pie_chart=pie_img_path, bar_chart=bar_chart_path)

    # context = {
    #     'percentage': impt_percent,
    #     # 'pie_img_path': pie_img_path,
    # }

    data_temp = Planning_temp.objects.get(plantype=plantype) # change ff to var that instead to type of planning
    add_recent_record(data_temp.og, data_temp.ds, data_temp.traveltime, data_temp.arrv)
    Planning_temp.objects.all().delete()

    context = {
        'data_temp': data_temp,
        'start': data_temp.start.strftime('%H:%M'),
        'arrv': data_temp.arrv.strftime('%H:%M')
    }

    return HttpResponse(template.render(context, request))

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

def back_to_home(request):
    return HttpResponseRedirect(reverse('index_home'))

def reset_temp_data(request):
    Planning_temp.objects.all().delete()
    return HttpResponseRedirect(reverse('index_home'))