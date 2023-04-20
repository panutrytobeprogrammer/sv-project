from django.urls import path
from . import views

urlpatterns = [
    # path('', views.login, name='login'),
    # # path('savedata/', views.save_data, name='savedata'),
    # path('register/', views.register, name='register'),
    # path('register/regist/', views.regist, name='regist'),
    # path('loggedin/', views.loggedin, name='loggedin'),
    # path('loggedin/<int:user_id>/', views.index, name='index_home'),
    # path('loggedin/<int:user_id>/reset_temp_data/', views.reset_temp_data, name='reset_temp_data'),
    # path('loggedin/<int:user_id>/map/', views.map_home, name='map_home'),
    # path('loggedin/<int:user_id>/recent/', views.recent_plan_seeall, name='recentplan'),
    # path('loggedin/<int:user_id>/soon/', views.soon, name='soon'),
    # path('loggedin/<int:user_id>/planning/', views.planning, name='planning'),
    # path('loggedin/<int:user_id>/planning/visualize/<str:plantype>', views.visualize, name='visualize'),
    # path('loggedin/<int:user_id>/planning/visualize/done/', views.back_to_home, name='done'),
    # path('loggedin/<int:user_id>/recentplanning/<int:plan_id>', views.planrecent, name='plannrecent'),
    # path('loggedin/<int:user_id>/planning/<int:plan_id>', views.planningfromrecent, name='planningfromrecent'),
    # # path('loggedin/<int:user_id>/<int:plan_id>/planning/visualize/<str:plantype>', views.visualize, name='visualize'),
    # # path('loggedin/<int:user_id>/<int:plan_id>/planning/visualize/done/', views.back_to_home, name='done'),

    path('', views.index, name='index_home'),
    path('reset_temp_data/', views.reset_temp_data, name='reset_temp_data'),
    path('map/', views.map_home, name='map_home'),
    path('recent/', views.recent_plan_seeall, name='recentplan'),
    path('soon/', views.soon, name='soon'),
    path('planning/', views.planning, name='planning'),
    path('planning/visualize/<str:plantype>', views.visualize, name='visualize'),
    path('planning/visualize/done/', views.visualize_done, name='done'),
    path('recentplanning/<int:plan_id>', views.planrecent, name='plannrecent'),
    path('planning/<int:plan_id>', views.planningfromrecent, name='planningfromrecent'),
]