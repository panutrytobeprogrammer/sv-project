from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Recentplan(models.Model):
    user_id = models.PositiveIntegerField()
    origin_name = models.CharField(max_length=255)
    origin_pos = models.CharField(max_length=255)
    destin_name = models.CharField(max_length=255)
    destin_pos = models.CharField(max_length=255)
    avg_time = models.PositiveIntegerField()
    timestamp = models.DateTimeField()

class location(models.Model):
    name = models.CharField(max_length=255)
    geometry = models.CharField(max_length=255)

class Location_time(models.Model):
    pass

class Appoint_default(models.Model):
    name = models.CharField(max_length=255)
    default_time = models.IntegerField()

class planning_to_visualize(models.Model):
    origin_name = models.CharField(max_length=255)
    destin_name = models.CharField(max_length=255)
    avg_time = models.PositiveIntegerField()
    percent = models.PositiveIntegerField()
    pie_chart = models.ImageField()
    bar_chart = models.ImageField()

class Planning_temp(models.Model):
    user_id = models.PositiveIntegerField()
    plantype = models.CharField(max_length=255)
    og = models.CharField(max_length=255)
    start = models.DateTimeField()
    ds = models.CharField(max_length=255)
    arrv = models.DateTimeField()
    traveltime = models.PositiveIntegerField()
    extratime = models.IntegerField()

class User_id(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=12)

class Varandma(models.Model):
    From = models.CharField(max_length=255)
    End = models.CharField(max_length=255)
    days = models.CharField(max_length=8)
    time = models.TimeField()
    ff = models.FloatField()
    avg = models.FloatField()
    p95 = models.FloatField()
    tti = models.FloatField()
    year = models.PositiveIntegerField()

# class User(AbstractUser):
#     user_key_id = models.CharField(max_length=8)