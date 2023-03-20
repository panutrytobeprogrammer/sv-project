from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_home'),
    path('reset_temp_data/', views.reset_temp_data, name='reset_temp_data'),
    path('map/', views.map_home, name='map_home'),
    path('recent/', views.recent_plan_seeall, name='recentplan'),
    path('soon/', views.soon, name='soon'),
    path('planning/', views.planning, name='planning'),
    path('planning/visualize/<str:plantype>', views.visualize, name='visualize'),
    path('planning/visualize/done/', views.back_to_home, name='done'),
]