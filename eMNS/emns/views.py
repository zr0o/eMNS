####################################################################################
### Bipul Ghimire
### email : thebipul79@gmail.com
#####################################################################################

from itertools import count
from random import choices
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from datetime import datetime
from .models import Device, Log
import time
import paramiko
from django.contrib.auth.decorators import login_required
from .resources import DeviceResource
from paramiko import SSHClient, AutoAddPolicy
import os

#for dashboard
@login_required(login_url='login')
def index(request):
    all_devices = Device.objects.all()
    ciscos = Device.objects.filter(vendor_type="cisco",)
    mikrotiks = Device.objects.filter(vendor_type="mikrotik")
    junipers = Device.objects.filter(vendor_type="juniper")
    log_activity = Log.objects.all()
    log_persentase = len(log_activity)*100/10000
    persentase_act = 'width:' + str(log_persentase) + '%'
    logsrec = Log.objects.all().order_by('-time')[:4]

    context = {
        'all_devices' : len(all_devices),
        'ciscos' : len(ciscos),
        'mikrotiks' : len(mikrotiks),
        'junipers' : len(junipers),
        'log_persentase': persentase_act,
        'logs': logsrec,
        'total_log': len(logsrec)
    }
    return render(request, 'emns/index.html', context)

#for command and control
@login_required(login_url='login')
def configt(request):
    #for configure terminal
   
    if request.method == "POST":
        result = []
        
        selected_device_id = request.POST.getlist('device_configt')
        cisco_command = request.POST['cisco_command'].splitlines()
        mikrotik_command = request.POST['mikrotik_command'].splitlines()
        juniper_command = request.POST['juniper_command'].splitlines()

        for x in selected_device_id:
            try:
                alat = get_object_or_404(Device, pk=x)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=alat.ip_address,username=alat.username,password=alat.password)

                if alat.vendor_type.lower() == 'cisco':
                    conn = ssh_client.invoke_shell()
                    conn.send("conf t\n")
                    for cmd in cisco_command:
                        conn.send(cmd + "\n")
                        time.slep(1)
                        output = conn.recv(65535)
                        result.append(output.decode())
                        log = Log(device_id=alat, host=alat.ip_address, action="Configure Terminal", status="Success", time=datetime.now(), messages="No Errors", commandline=cmd)
                        log.save()

                elif alat.vendor_type.lower() == 'juniper':
                    conn = ssh_client.invoke_shell()
                    conn.send("cli\n")
                    for cmd in juniper_command:
                        ssh_client.exec_command(cmd + "\n")
                        time.slep(3)
                        output = conn.recv(1000)
                        result.append(output.decode())
                        log = Log(device_id=alat, host=alat.ip_address, action="Configure Terminal", status="Success", time=datetime.now(), messages="No Errors", commandline=cmd)
                        log.save()

                else:
                    for cmd in mikrotik_command:
                        ssh_client.exec_command(cmd)
                        log = Log(device_id=alat, host=alat.ip_address, action="Configure Terminal", status="Success", time=datetime.now(), messages="No Errors", commandline=cmd)
                        log.save()
            except Exception as e:
                    log = Log(device_id=alat, host=alat.ip_address, action="Configure Terminal", status="Failed", time=datetime.now(), messages=e, commandline=cisco_command)
                    log.save()
            return redirect('emns/configt.html')
        
        result = "\n".join(result)
        return render(request, 'emns/verifcli.html', {'result':result})
    
    else:
        devi = Device.objects.all()
        logsrec = Log.objects.all().order_by('-time')[:4]
        context = {
            'total_devices' : len(devi),
            'devi' : devi,
            'total_log' : len(logsrec),
            'mode' : 'conft',
            'logs' : logsrec
            }
        return render(request, 'emns/conft.html', context)
#for total devices list
@login_required
def deviceslist(request):
    total_devices=Device.objects.all()
    logsrec = Log.objects.all().order_by('-time')[:4]
    context = {
        'total_devices': len(total_devices),
        'list_devices': total_devices,
        'total_log': len(logsrec),
        'logs': logsrec
    }
    return render(request,'emns/devices-list.html', context)

#for cisco devices list
@login_required
def ciscolist(request):
    cisco_devices = Device.objects.filter(vendor_type="cisco",)
    logsrec = Log.objects.all().order_by('-time')[:4]
    context = {
        'cisco_devices': len(cisco_devices),
        'list_devices': cisco_devices,
        'total_log': len(logsrec),
        'logs': logsrec
    }
    return render(request, 'emns/cisco-list.html', context)

#for miktotik devices list
@login_required
def mikrotiklist(request):
    mikrotik_devices = Device.objects.filter(vendor_type="mikrotik")
    logsrec = Log.objects.all().order_by('-time')[:4]
    context = {
        'mikrotik_devices': len(mikrotik_devices),
        'list_devices': mikrotik_devices,
        'total_log': len(logsrec),
        'logs': logsrec
    }
    return render(request, 'emns/mikrotik-list.html', context)

#for juniper devices list
@login_required
def juniperlist(request):
    juniper_devices = Device.objects.filter(vendor_type="juniper")
    logsrec = Log.objects.all().order_by('-time')[:4]
    context = {
        'juniper_devices': len(juniper_devices),
        'list_devices': juniper_devices,
        'total_log': len(logsrec),
        'logs': logsrec
    }
    return render(request, 'emns/juniper-list.html', context)

#for logs
@login_required
def log(request):
    logsrec = Log.objects.all().order_by('-time')[:4]
    logs = Log.objects.all().order_by('-time')[:30]
    context = {
        'logs': logsrec,
        'total_log': len(logsrec),
        'logs1': logs
    }
    return render(request, 'emns/log.html', context)

#for save configuration
@login_required
def saveconf(request):
    #for save conf
    if request.method == "POST":
        result = []
        selected_devices_id = request.POST.getlist('cxb_device')
        sleept = int(request.POST['paramts'])
        for x in selected_devices_id:
            try:
                alat = get_object_or_404(Device, pk=x)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=alat.ip_address, username=alat.username, password=alat.password, allow_agent=False)
                conn = ssh_client.invoke_shell()
                conn.send('terminal length 0\n')
                result.append("Result on {}".format(alat.ip_address))
                conn.send('write\n')
                time.sleep(sleept)
                output = conn.recv(65535)
                result.append(output.decode())
                log = Log(device_id=alat, host=alat.ip_address, action="Save Configurations", status="Success", time=datetime.now(), messages="No Errors", commandline="write memory")
                log.save()
            except Exception as e:
                log = Log(device_id=alat, host=alat.ip_address, action="Save Configurations", status="Failed", time=datetime.now(), messages=e, commandline="write memory")
                log.save()
        result = "\n".join(result)
        return render(request, 'emns/verify_result.html', {'result':result})     
    else:
        devi = Device.objects.all()
        logsrec = Log.objects.all().order_by('-time')[:4]
        context = {
            'total_devices': len(devi),
            'devi': devi,
            'mode': 'Save Configuration',
            'total_log': len(logsrec),
            'logs': logsrec
        }
        return render(request, 'emns/saveconf.html', context)

#for backup configuration
@login_required
def backupconf(request):
    #for backup conf
    if request.method == "POST":
        result = []
        selected_devices_id = request.POST.getlist('cxb_device')
        sleept = int(request.POST['paramts'])
        for x in selected_devices_id:
            try:
                alat = get_object_or_404(Device, pk=x)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=alat.ip_address, username=alat.username, password=alat.password, allow_agent=False)
                conn = ssh_client.invoke_shell()
                conn.send('terminal length 0\n')
                result.append("Result on {}".format(alat.ip_address))
                conn.send('copy run tftp:10.10.10.254\n')
                time.sleep(sleept)
                output = conn.recv(65535)
                result.append(output.decode())
                log = Log(device_id=alat, host=alat.ip_address, action="BackUp Configurations", status="Success", time=datetime.now(), messages="No Errors", commandline="write memory")
                log.save()
            except Exception as e:
                log = Log(device_id=alat, host=alat.ip_address, action="BackUp Configurations", status="Failed", time=datetime.now(), messages=e, commandline="write memory")
                log.save()
        result = "\n".join(result)
        return render(request, 'emns/verify_result.html', {'result':result})     
    else:
        devi = Device.objects.all()
        logsrec = Log.objects.all().order_by('-time')[:4]
        context = {
            'total_devices': len(devi),
            'devi': devi,
            'mode': 'BackUp Configuration',
            'total_log': len(logsrec),
            'logs': logsrec
        }
        return render(request, 'emns/backupconf.html', context)

#for load configuration
@login_required
def loadconf(request):
    #for loading conf
    if request.method == "POST":
        result = []
        selected_devices_id = request.POST.getlist('cxb_device')
        sleept = int(request.POST['paramts'])
        for x in selected_devices_id:
            try:
                alat = get_object_or_404(Device, pk=x)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=alat.ip_address, username=alat.username, password=alat.password, allow_agent=False)
                conn = ssh_client.invoke_shell()
                conn.send('terminal length 0\n')
                result.append("Result on {}".format(alat.ip_address))
                conn.send('copy tftp:10.10.10.254 run\n')
                time.sleep(sleept)
                output = conn.recv(65535)
                result.append(output.decode())
                log = Log(device_id=alat, host=alat.ip_address, action="Load Configurations", status="Success", time=datetime.now(), messages="No Errors", commandline="write memory")
                log.save()
            except Exception as e:
                log = Log(device_id=alat, host=alat.ip_address, action="Load Configurations", status="Failed", time=datetime.now(), messages=e, commandline="write memory")
                log.save()
        result = "\n".join(result)
        return render(request, 'emns/verify_result.html', {'result':result})     
    else:
        devi = Device.objects.all()
        logsrec = Log.objects.all().order_by('-time')[:4]
        context = {
            'total_devices': len(devi),
            'devi': devi,
            'mode': 'Load Configuration',
            'total_log': len(logsrec),
            'logs': logsrec
        }
        return render(request, 'emns/loadconf.html', context)

#for ping
@login_required
def pinging(request):
    if request.method == "POST":
        selected_devices_id = request.POST.getlist('cxb_device')
        result = []
        for x in selected_devices_id:
            alat = get_object_or_404(Device, pk=x)
            response = os.popen(f"ping {alat.ip_address}").read()
            if "Received = 4" in response:
                result.append(f"UP {alat.ip_address} Ping OK")
            else:
                result.append(f"DOWN {alat.ip_address} Ping Timeout")
        result = "\n".join(result) 
        return render(request, 'emns/verify_result.html', {'result':result})     
    else:
        devi = Device.objects.all()
        logsrec = Log.objects.all().order_by('-time')[:4]
        context = {
            'total_devices': len(devi),
            'devi': devi,
            'mode': 'Pinging',
            'total_log': len(logsrec),
            'logs': logsrec
        }
        return render(request, 'emns/pinging.html', context)       

#for reload
def reload(request):
    if request.method == "POST":
        result = []
        selected_devices_id = request.POST.getlist('cxb_device')
        sleept = int(request.POST['paramts'])
        for x in selected_devices_id:
            try:
                alat = get_object_or_404(Device, pk=x)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=alat.ip_address, username=alat.username, password=alat.password, allow_agent=False)
                conn = ssh_client.invoke_shell()
                conn.send('terminal length 0\n')
                #conn.send('reload\n')
                conn.send('reload\n')
                time.sleep(sleept)
                conn.send('yes\n')
                time.sleep(sleept)
                conn.send('yes\n')
                output = conn.recv(65535)
                #result.append("Result on {}".format(alat.ip_address))
                result.append(output.decode())
                log = Log(device_id=alat, host=alat.ip_address, action="Reload", status="Success", time=datetime.now(), messages="No Errors", commandline="reload")
                log.save()
            except Exception as e:
                log = Log(device_id=alat, host=alat.ip_address, action="Reload", status="Failed", time=datetime.now(), messages=e, commandline="reload")
                log.save()
        result = "\n".join(result)
        return render(request, 'emns/verify_result.html', {'result':result})     
    else:
        devi = Device.objects.all()
        logsrec = Log.objects.all().order_by('-time')[:4]
        context = {
            'total_devices': len(devi),
            'devi': devi,
            'mode': 'Reload Devices',
            'total_log': len(logsrec),
            'logs': logsrec
        }
        return render(request, 'emns/reload.html', context)

#for verify 
@login_required
def verfcli(request, id):
    #for verify cli
    logcli = Log.objects.get(pk = id)
    return render(request, 'emns/verify_cli.html', {'logcli': logcli})

#for verify result
@login_required
def verifrslt(request, id):
    #for verify cli
    logcli = Log.objects.get(pk = id)
    return render(request, 'emns/verify_result.html', {'logcli': logcli})

