####################################################################################
### Bipul Ghimire
### email : thebipul79@gmail.com
#####################################################################################
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, 'emns/index.html')