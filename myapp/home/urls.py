from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('map/', views.map_home, name='map_home'),
    path('recent/', views.recent_plan_seeall, name='recentplan'),
    path('soon/', views.soon, name='soon'),
    path('planning/', views.planning, name='planning'),
    path('planning/visualize/', views.visualize, name='visualize'),
]