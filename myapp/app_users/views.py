from django.shortcuts import render
from app_users.forms import RegisterForm
from django.template import loader
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth import login
from django.urls import reverse

# Create your views here.

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
        'form':form
    }
    return render(request, 'app_users/register.html', context)