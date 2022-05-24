
# Create your views here.
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#for registeration
def register(request):
    if request.user.is_authenticated:
        username = request.user
        messages.info(request, f'Welcome {username} ! Have a great time doing recon.')
        return redirect('index')
    else:
        form = UserRegisterForm()
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, f'Successfully created an account for.' + user)
                return redirect('login')

        context = {'form': form}
        return render(request, 'users/register.html', context)

#for login
def loginPage(request):
    if request.user.is_authenticated:
        username = request.user
        messages.info(request, f'Welcome  !')
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.warning(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'users/login.html', context)

#for logout
def logoutUser(request):
    logout(request)
    username = request.user
    messages.info(request, f'Thank you for visiting us. Have a good day.')
    return redirect('login')
