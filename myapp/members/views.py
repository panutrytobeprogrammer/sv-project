from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Members
from django.urls import reverse

# Create your views here.
def index(request):
    mymembers = Members.objects.all().values()
    template = loader.get_template('index.html')
    context = {
        'mymembers': mymembers
    }
    return HttpResponse(template.render(context, request))

def add(request):
    template = loader.get_template('add.html')
    return HttpResponse(template.render({}, request))

def addrecord(request):
    firstname = request.POST['first']
    lastname = request.POST['last']
    member = Members(firstname=firstname, lastname=lastname)
    member.save()
    return HttpResponseRedirect(reverse('index'))

def delete(request, id):
    members = Members.objects.get(id=id)
    members.delete()
    return HttpResponseRedirect(reverse('index'))

def update(request, id):
    mymember = Members.objects.get(id=id)
    template = loader.get_template('update.html')
    context = {
        'mymember': mymember
    }
    return HttpResponse(template.render(context, request))

def updaterecord(request, id):
    firstname = request.POST['first']
    lastname = request.POST['last']
    member = Members.objects.get(id=id)
    member.firstname = firstname
    member.lastname = lastname
    member.save()
    return HttpResponseRedirect(reverse('index'))
