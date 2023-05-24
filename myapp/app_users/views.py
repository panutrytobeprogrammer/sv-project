from django.shortcuts import render
from app_users.forms import RegisterForm
from django.template import loader
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth import login
from django.urls import reverse
import os

# Create your views here.
font_api = str(os.getenv('FONT_API'))
gg_ana = str(os.getenv('GG_ANA'))

def register(request: HttpRequest):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            # return HttpResponseRedirect(reverse('index_home'))
    else:
        form = RegisterForm()

    form = RegisterForm()
    # template = loader.get_template('app_users/register.html')
    context = {
        'form':form,
        'font_api': font_api,
        'gg_ana': gg_ana,
    }
    return render(request, 'app_users/register.html', context)