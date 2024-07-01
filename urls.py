from django.urls import path
from . import views

urlpatterns =[
    path('', views.Landing_0, name='Landing_0'),
    path('aLanding', views.aLanding, name='aLanding'),
   
    path('Register_2/', views.Register_2, name='Register_2'),
    path('Login_3/', views.Login_3, name='Login_3'),

    path('input1/', views.input1, name='input1'),
    path('output', views.output, name='output'),

    path('Logout/', views.Logout, name='Logout'),
    #path('output1/', views.output1, name='output1'),
]