from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import get_user
from .models import Recentplan, location, Planning_temp, User_id, Varandma
from django.urls import reverse
import datetime
from .program_func import *
import os


# Create your views here.

map_api = str(os.getenv('MAP_API'))
font_api = str(os.getenv('FONT_API'))
gg_ana = str(os.getenv('GG_ANA'))

def index(request):
    user_id = get_user(request).id
    # print('---------------------------------------')
    # print('user id:', user_id)
    # print('---------------------------------------')
    print(f'[{datetime.datetime.now().strftime("%d/%b/%Y %H:%M:%S")}] [user_id: {user_id}] index_process')
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
        'location_data': location_data,
        'map_api': map_api,
        'font_api': font_api,
        'gg_ana': gg_ana,
    }
    return HttpResponse(template.render(context, request))

def map_home(request):
    print(f'{datetime.datetime.now()}: map')
    template = loader.get_template('map.html')
    return HttpResponse(template.render())

def add_recent_record(user_id, og_name, ds_name, avg_time, plantime):
    og_pos = location.objects.get(name=og_name)
    ds_pos = location.objects.get(name=ds_name)
    plan = Recentplan(user_id=user_id, origin_name=og_name, origin_pos=og_pos, destin_name=ds_name, destin_pos=ds_pos, avg_time=avg_time, timestamp=str(plantime))
    plan.save()

def planning(request):
    user_id = get_user(request).id
    print(f'[{datetime.datetime.now().strftime("%d/%b/%Y %H:%M:%S")}] [user_id: {user_id}] planning start')
    Planning_temp.objects.filter(user_id=user_id).all().delete()
    # load template
    template = loader.get_template('planning.html')
    origin_name = request.POST['origin_plan']
    destin_name = request.POST['destination_plan']
    plantime_date = request.POST['plantime_date']
    # print('date:', plantime_date)
    plantime_time = request.POST['plantime_time']
    # print('time:', plantime_time)
    origin_s = s_name(origin_name)
    destin_s = s_name(destin_name)

    # if pd.isna(pd.Timestamp(plantime_date)) or pd.isna(pd.Timestamp(plantime_time)):
    #     plantime = datetime.datetime.now() + datetime.timedelta(hours=7)
    if len(plantime_date) == 0 and len(plantime_time) == 0:
        plantime = datetime.datetime.now() + datetime.timedelta(hours=7)
    elif len(plantime_time) == 0:
        plantime = f'{plantime_date} {(datetime.datetime.now() + datetime.timedelta(hours=7)).time()}'
    elif len(plantime_date) == 0:
        plantime = f'{datetime.datetime.now().date()} {plantime_time}'
    else:
        plantime = pd.to_datetime(f'{plantime_date} {plantime_time}')

    # query time
    plantime = pd.to_datetime(plantime)
    time = query_time_v2(route=f'{origin_s}_{destin_s}', dt=plantime)
    ff_time = time['ff_time']
    avg_time = time['avg_time']
    p95_time = time['p95_time']

    dep_time_ff = plantime - datetime.timedelta(minutes=ff_time)
    dep_time_avg = plantime - datetime.timedelta(minutes=avg_time)
    dep_time_p95 = plantime - datetime.timedelta(minutes=p95_time)

    # save to planning temp table
    Planning_temp(user_id=user_id, plantype='Safe time', og=origin_name, start=dep_time_p95, ds=destin_name, arrv=plantime, traveltime=p95_time,  extratime=p95_time-avg_time).save()
    Planning_temp(user_id=user_id, plantype='Usual time', og=origin_name, start=dep_time_avg, ds=destin_name, arrv=plantime, traveltime=avg_time, extratime=0).save()
    Planning_temp(user_id=user_id, plantype='Unsafe time', og=origin_name, start=dep_time_ff, ds=destin_name, arrv=plantime, traveltime=ff_time, extratime=ff_time-avg_time).save()
    
    og_pos = location.objects.get(name=origin_name).geometry.split(',')
    ds_pos = location.objects.get(name=destin_name).geometry.split(',')

    dep_time = Planning_temp.objects.filter(user_id=user_id).all()

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
        'map_api': map_api,
        'font_api': font_api,
        'gg_ana': gg_ana,
    }
    print(f'[{datetime.datetime.now().strftime("%d/%b/%Y %H:%M:%S")}] [user_id: {user_id}] planning end')
    return HttpResponse(template.render(context, request))

def visualize(request, plantype):
    user_id = get_user(request).id
    print(f'[{datetime.datetime.now().strftime("%d/%b/%Y %H:%M:%S")}] [user_id: {user_id}] visualize start')
    template = loader.get_template('viz2.html')

    data_temp = Planning_temp.objects.filter(user_id=user_id).get(plantype=plantype)
    # add_recent_record(user_id, data_temp.og, data_temp.ds, data_temp.traveltime, data_temp.arrv)
    time_graph = graph_time(data_temp.og, data_temp.ds, data_temp.arrv)
    # label = time_graph['time']
    data = time_graph['tti']

    og_pos = location.objects.get(name=data_temp.og).geometry.split(',')
    ds_pos = location.objects.get(name=data_temp.ds).geometry.split(',')

    extratime = data_temp.extratime
    txt_et2 = ''
    if plantype[:6] == 'Unsafe':
        txt_et = f'This is the fastest time you will arrive,'
        txt_et2 = 'but you might be late.'
    elif plantype[:4] == 'Safe':
        txt_et = f"Departing at { data_temp.start.strftime('%H:%M') }, you most likely arrive on time."
    else:
        txt_et = f"After { data_temp.start.strftime('%H:%M') }, you are likely to be late."
    
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
        'txt_et2':txt_et2,
        'ttt':ttt,
        'extratime':extratime,
        'plantype': plantype,
        # 'now':(data_temp.start - datetime.datetime.now() - datetime.timedelta(hours=7)),
        'map_api': map_api,
        'font_api': font_api,
        'gg_ana': gg_ana,
    }
    print(f'[{datetime.datetime.now().strftime("%d/%b/%Y %H:%M:%S")}] [user_id: {user_id}] visualize end')
    return HttpResponse(template.render(context, request))

def recent_plan_seeall(request):
    user_id = get_user(request).id
    print(f'[{datetime.datetime.now().strftime("%d/%b/%Y %H:%M:%S")}] [user_id: {user_id}] recent plan see all')
    template = loader.get_template('recent.html')
    result_exist = Recentplan.objects.filter(user_id=user_id)
    if result_exist.exists():
        data = result_exist.all().order_by('-id')
    else:
        data = {'origin_name': 'None', 'destin_name': 'None', 'timestamp': 'None'}
    context = {
        'recent_data': data,
        'map_api': map_api,
        'font_api': font_api,
        'gg_ana': gg_ana,
    }
    return HttpResponse(template.render(context, request))

def soon(request):
    user_id = get_user(request).id
    print(f'[{datetime.datetime.now().strftime("%d/%b/%Y %H:%M:%S")}] [user_id: {user_id}] soon page')
    template = loader.get_template('comingsoon.html')
    return HttpResponse(template.render())

def visualize_done(request):
    user_id = get_user(request).id
    data_temp = Planning_temp.objects.filter(user_id=user_id).get(plantype='Usual time')
    add_recent_record(user_id, data_temp.og, data_temp.ds, data_temp.traveltime, data_temp.arrv)
    Planning_temp.objects.filter(user_id=user_id).all().delete()
    url = reverse('index_home')
    print(f'[{datetime.datetime.now().strftime("%d/%b/%Y %H:%M:%S")}] [user_id: {user_id}] done')
    return HttpResponseRedirect(url)

# def back_to_home(request):
#     user_id = get_user(request).id
#     Planning_temp.objects.filter(user_id=user_id).all().delete()
#     url = reverse('index_home')
#     return HttpResponseRedirect(url)

def reset_temp_data(request):
    user_id = get_user(request).id
    print(f'[{datetime.datetime.now().strftime("%d/%b/%Y %H:%M:%S")}] [user_id: {user_id}] reset temp data')
    Planning_temp.objects.filter(user_id=user_id).all().delete()
    url = reverse('index_home')
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

def planrecent(request, plan_id):
    template = loader.get_template('planrecent.html')
    temp = Recentplan.objects.get(id=plan_id)
    context = {
        'plan_temp': temp,
        'plan_id': plan_id,
        'map_api': map_api,
        'font_api': font_api,
        'gg_ana': gg_ana,
    }
    return HttpResponse(template.render(context, request))

def planningfromrecent(request, plan_id):
    user_id = get_user(request).id
    Planning_temp.objects.filter(user_id=user_id).all().delete()
    # load template
    template = loader.get_template('planning.html')

    temp = Recentplan.objects.get(id=plan_id)

    origin_name = temp.origin_name
    destin_name = temp.destin_name
    plantime_date = request.POST['plantime_date']
    print('date:', plantime_date)
    plantime_time = request.POST['plantime_time']
    print('time:', plantime_time)
    origin_s = s_name(origin_name)
    destin_s = s_name(destin_name)

    if len(plantime_date) == 0 and len(plantime_time) == 0:
        plantime = datetime.datetime.now() + datetime.timedelta(hours=7)
    elif len(plantime_time) == 0:
        plantime = f'{plantime_date} {(datetime.datetime.now() + datetime.timedelta(hours=7)).time()}'
    elif len(plantime_date) == 0:
        plantime = f'{datetime.datetime.now().date()} {plantime_time}'
    else:
        plantime = pd.to_datetime(f'{plantime_date} {plantime_time}')

    # query time
    plantime = pd.to_datetime(plantime)
    time = query_time_v2(route=f'{origin_s}_{destin_s}', dt=plantime)
    ff_time = time['ff_time']
    avg_time = time['avg_time']
    p95_time = time['p95_time']

    dep_time_ff = plantime - datetime.timedelta(minutes=ff_time)
    dep_time_avg = plantime - datetime.timedelta(minutes=avg_time)
    dep_time_p95 = plantime - datetime.timedelta(minutes=p95_time)

    # save to planning temp table
    Planning_temp(user_id=user_id, plantype='Safe time', og=origin_name, start=dep_time_p95, ds=destin_name, arrv=plantime, traveltime=p95_time,  extratime=p95_time-avg_time).save()
    Planning_temp(user_id=user_id, plantype='Usual time', og=origin_name, start=dep_time_avg, ds=destin_name, arrv=plantime, traveltime=avg_time, extratime=0).save()
    Planning_temp(user_id=user_id, plantype='Unsafe time', og=origin_name, start=dep_time_ff, ds=destin_name, arrv=plantime, traveltime=ff_time, extratime=ff_time-avg_time).save()
    
    og_pos = location.objects.get(name=origin_name).geometry.split(',')
    ds_pos = location.objects.get(name=destin_name).geometry.split(',')

    dep_time = Planning_temp.objects.filter(user_id=user_id).all()

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
        'map_api': map_api,
        'font_api': font_api,
        'gg_ana': gg_ana,
    }
    print(f'{datetime.datetime.now()}: planning end')
    return HttpResponse(template.render(context, request))


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

# def save_data(request):
#     df = pd.read_csv('home/df_varandma.csv')
#     for i,row in df.iterrows():
#         From = row['from']
#         End = row['end']
#         days = row['days']
#         time = row['time']
#         ff = row['freeflow traveltime']
#         avg = row['average traveltime']
#         p95 = row['95th percentile']
#         tti = row['Traveltime Index']
#         year = row['year']
#         Varandma(From=From, End=End, days=days, time=time, ff=ff, avg=avg, p95=p95, tti=tti, year=year).save()
#         print(datetime.datetime.now(), ': round', i)
#     return HttpResponseRedirect(reverse('login'))