from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate, login
from .models import Recentplan, location, Planning_temp, User_id
from django.urls import reverse
import datetime
from .program_func import *



# Create your views here.

def index(request, user_id):
    # load template
    template = loader.get_template('home.html')
    # get recent data
    result_exist = Recentplan.objects.filter(user_id=user_id)
    if result_exist.exists():
        data_recent = Recentplan.objects.filter(user_id=user_id).last()
    else:
        data_recent = {'origin_name': 'None', 'destin_name': 'None', 'timestamp': 'None'}
    location_data = location.objects.all().values()
    context = {
        'last_data': data_recent,
        'location_data': location_data
    }
    return HttpResponse(template.render(context, request))

def map_home(request):
    template = loader.get_template('map.html')
    return HttpResponse(template.render())

def add_recent_record(user_id, og_name, ds_name, avg_time, plantime):
    og_pos = location.objects.get(name=og_name)
    ds_pos = location.objects.get(name=ds_name)
    plan = Recentplan(user_id=user_id, origin_name=og_name, origin_pos=og_pos, destin_name=ds_name, destin_pos=ds_pos, avg_time=avg_time, timestamp=str(plantime))
    plan.save()

def planning(request, user_id):
    Planning_temp.objects.filter(user_id=user_id).all().delete()
    # load template
    template = loader.get_template('planning.html')
    origin_name = request.POST['origin_plan']
    destin_name = request.POST['destination_plan']
    plantime = request.POST['plantime']
    origin_s = s_name(origin_name)
    destin_s = s_name(destin_name)

    # query time
    if pd.isna(pd.Timestamp(plantime)):
        plantime = datetime.datetime.now() + datetime.timedelta(hours=7)
    plantime = pd.to_datetime(plantime)
    time = query_time(route=f'{origin_s}_{destin_s}', dt=plantime)
    ff_time = time['ff_time']
    avg_time = time['avg_time']
    p95_time = time['p95_time']

    dep_time_ff = plantime - datetime.timedelta(minutes=ff_time)
    dep_time_avg = plantime - datetime.timedelta(minutes=avg_time)
    dep_time_p95 = plantime - datetime.timedelta(minutes=p95_time)

    # save to planning temp table
    Planning_temp(user_id=user_id, plantype='Unsafe', og=origin_name, start=dep_time_ff, ds=destin_name, arrv=plantime, traveltime=ff_time, extratime=ff_time-avg_time).save()
    Planning_temp(user_id=user_id, plantype='Usual', og=origin_name, start=dep_time_avg, ds=destin_name, arrv=plantime, traveltime=avg_time, extratime=0).save()
    Planning_temp(user_id=user_id, plantype='Safe', og=origin_name, start=dep_time_p95, ds=destin_name, arrv=plantime, traveltime=p95_time,  extratime=p95_time-avg_time).save()
    
    og_pos = location.objects.get(name=origin_name).geometry.split(',')
    ds_pos = location.objects.get(name=destin_name).geometry.split(',')

    dep_time = Planning_temp.objects.filter(user_id=user_id).all().order_by('-id')

    context = {
        'origin_name':origin_name,
        'destin_name':destin_name,
        'time':time,
        'now':plantime.strftime('%H:%M'),
        'dep_time_ff':dep_time_ff.strftime('%H:%M'),
        'dep_time_avg':dep_time_avg.strftime('%H:%M'),
        'dep_time_p95':dep_time_p95.strftime('%H:%M'),
        'dep_time': dep_time,
        'og_pos_lon': og_pos[1][:-1],
        'og_pos_lat': og_pos[0][1:],
        'ds_pos_lon': ds_pos[1][:-1],
        'ds_pos_lat': ds_pos[0][1:],
    }
    return HttpResponse(template.render(context, request))

def visualize(request, plantype, user_id):
    template = loader.get_template('visualize.html')

    data_temp = Planning_temp.objects.filter(user_id=user_id).get(plantype=plantype)
    add_recent_record(user_id, data_temp.og, data_temp.ds, data_temp.traveltime, data_temp.arrv)
    time_graph = graph_time(data_temp.og, data_temp.ds, data_temp.arrv)
    # label = time_graph['time']
    data = time_graph['tti']

    og_pos = location.objects.get(name=data_temp.og).geometry.split(',')
    ds_pos = location.objects.get(name=data_temp.ds).geometry.split(',')

    extratime = data_temp.extratime
    if plantype == 'Unsafe':
        txt_et = f'Save {abs(extratime)} min'
    elif plantype == 'Safe':
        txt_et = f'Extra time {extratime} min'
    else:
        txt_et = 'No extra time'
    
    ttt = data_temp.traveltime - extratime

    context = {
        'data_temp': data_temp,
        'start': data_temp.start.strftime('%H:%M'),
        'arrv': data_temp.arrv.strftime('%H:%M'),
        'data': data,
        'og_pos_lon': og_pos[1][:-1],
        'og_pos_lat': og_pos[0][1:],
        'ds_pos_lon': ds_pos[1][:-1],
        'ds_pos_lat': ds_pos[0][1:],
        'txt_et':txt_et,
        'ttt':ttt,
        'extratime':extratime,
    }

    return HttpResponse(template.render(context, request))

def recent_plan_seeall(request, user_id):
    template = loader.get_template('recent.html')
    result_exist = Recentplan.objects.filter(user_id=user_id)
    if result_exist.exists():
        data = result_exist.all().order_by('-id')
    else:
        data = {'origin_name': 'None', 'destin_name': 'None', 'timestamp': 'None'}
    context = {
        'recent_data': data
    }
    return HttpResponse(template.render(context, request))

def soon(request):
    template = loader.get_template('comingsoon.html')
    return HttpResponse(template.render())

def back_to_home(request, user_id):
    Planning_temp.objects.filter(user_id=user_id).all().delete()
    url = reverse('index_home', kwargs={'user_id':user_id})
    return HttpResponseRedirect(url)

def reset_temp_data(request, user_id):
    Planning_temp.objects.filter(user_id=user_id).all().delete()
    url = reverse('index_home', kwargs={'user_id':user_id})
    return HttpResponseRedirect(url)

def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def loggedin(request):
    template = loader.get_template('loggedin.html')
    username = request.POST['username']
    password = request.POST['password']
    result_exist = User_id.objects.filter(username=username)
    if result_exist.exists():
        user_id = User_id.objects.get(username=username).id
        if password == result_exist.get(username=username).password:
            context = {
                'user_id': user_id,
                'username': username
            }
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect(reverse('login'))
    else: return HttpResponseRedirect(reverse('login'))

def register(request):
    template = loader.get_template('register.html')
    return HttpResponse(template.render())

def regist(request):
    username = request.POST['username']
    password = request.POST['password']
    checkpass = request.POST['checkpass']
    result_exist = User_id.objects.filter(username=username)
    User_id(username=username, password=password).save()
    return HttpResponseRedirect(reverse('login'))


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             error_message = "Invalid username or password."
#     else:
#         error_message = ""
#     return render(request, 'login.html', {'error_message': error_message})