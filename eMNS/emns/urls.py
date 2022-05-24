####################################################################################
### Bipul Ghimire
### email : thebipul79@gmail.com
#####################################################################################
import imp
from django.contrib import admin
from . import views
from django.urls import path
from users import views as users_views

urlpatterns = [
    path('', views.index, name='index'), 
    path('login/', users_views.loginPage, name='login'),
    path('register/', users_views.register, name='register'),
    path('configt/', views.configt, name='configt'),
    path('deviceslist/', views.deviceslist, name='deviceslist'),
    path('ciscolist/', views.ciscolist, name='ciscolist'),
    path('mikrotiklist/', views.mikrotiklist, name='mikrotiklist'),
    path('juniperlist/', views.juniperlist, name='juniperlist'),
    path('log/', views.log, name='log'),
    path('saveconf/', views.saveconf, name='saveconf'),
    path('loadconf/', views.loadconf, name='loadconf'),
    path('backupconf/', views.backupconf, name='backupconf'),
    path('pinging/', views.pinging, name='pinging'),
    path('reload/', views.reload, name='reload'),
    path('verifcli/<int:id>', views.verfcli, name='verifcli'),
    path('verifrslt/<int:id>)',views.verifrslt, name='verifrslt')
]
