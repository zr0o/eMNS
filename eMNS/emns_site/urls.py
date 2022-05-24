####################################################################################
### Bipul Ghimire
### email : thebipul79@gmail.com
#####################################################################################
from django.contrib import admin
from django.urls import path, include

import users
from users import views as users_views

from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', include('emns.urls')),
    path('login/', users_views.loginPage, name='login'),
    path('admin/', admin.site.urls),
    path('logout/', users_views.logoutUser, name='logout') 
]

urlpatterns += staticfiles_urlpatterns()