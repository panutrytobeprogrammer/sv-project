from django.db import models

# Create your models here.
class Recentplan(models.Model):
    user_id = models.PositiveIntegerField()
    origin_name = models.CharField(max_length=255)
    origin_pos = models.CharField(max_length=255)
    destin_name = models.CharField(max_length=255)
    destin_pos = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

class location(models.Model):
    location_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    geometry = models.CharField(max_length=255)