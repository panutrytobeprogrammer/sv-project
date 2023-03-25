from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register/regist/', views.regist, name='regist'),
    path('loggedin/', views.loggedin, name='loggedin'),
    path('loggedin/<int:user_id>/', views.index, name='index_home'),
    path('loggedin/<int:user_id>/reset_temp_data/', views.reset_temp_data, name='reset_temp_data'),
    path('loggedin/<int:user_id>/map/', views.map_home, name='map_home'),
    path('loggedin/<int:user_id>/recent/', views.recent_plan_seeall, name='recentplan'),
    path('loggedin/<int:user_id>/soon/', views.soon, name='soon'),
    path('loggedin/<int:user_id>/planning/', views.planning, name='planning'),
    path('loggedin/<int:user_id>/planning/visualize/<str:plantype>', views.visualize, name='visualize'),
    path('loggedin/<int:user_id>/planning/visualize/done/', views.back_to_home, name='done'),
]