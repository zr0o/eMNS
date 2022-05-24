####################################################################################
### Bipul Ghimire
### email : thebipul79@gmail.com
#####################################################################################

from __future__ import unicode_literals
from email.policy import default
import ipaddress
from logging import PlaceHolder
from pickle import FALSE
from random import choices
from unicodedata import name
from unittest.util import _MAX_LENGTH
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

#for input field in adding devices
class Device(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=True, verbose_name='ID')
    ip_address = models.GenericIPAddressField(help_text="xxx.xxx.xxx.xxx")
    subnetmask = models.GenericIPAddressField(help_text="000.000.000.000")
    hostname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    sshport = models.IntegerField(default=22)
    
    #for chosing vendor
    TYPE_CHOICES1 = (
        ('cisco', 'Cisco'),
        ('mikrotik', 'MikroTik'),
        ('juniper', 'Juniper')
    )
    vendor_type = models.CharField(max_length=255, choices=TYPE_CHOICES1, blank=False)
    
    #for choosing the device type
    TYPE_CHOICES2 = (
        ('router', 'Router'),
        ('switch', 'Switch')
    )
    device_type = models.CharField(max_length=255, choices=TYPE_CHOICES2, blank=False)

    #fot choosing the device series
    SERIES_DEVICES = (
        ('Cisco Router 3725 Series','Cisco Router 3725 Series'),
        ('Cisco Router 7200 Series','Cisco Router 7200 Series'),
        ('Cisco Router 7600 Series','Cisco Router 7600 Series'),
        ('Cisco Catalyst 2960 Series','Cisco Catalyst 2960 Series'),
        ('Cisco Catalyst 3850 Series','Cisco Catalyst 3850 Series'),
        ('Juniper Router ACX7100 Series','Juniper Router ACX7100 Series'),
        ('Juniper Router J6350 Series','Juniper Router J6350 Series'),
        ('Juniper Switch EX Series','Juniper Switch EX Series'),
        ('MikroTik Router CCR1036 Series','MikroTik Router CCR1036 Series'),
        ('MikroTik Router CCR2004 Series','MikroTik Router CCR2004 Series'),
        ('MikroTik Switch CRS310 Series','MikroTik Switch CRS310 Series')
    )
    device_series = models.CharField(max_length=255, choices=SERIES_DEVICES, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.id, self.ip_address, self.hostname, self.vendor_type, self.device_type)

#for storing logs
class Log(models.Model):
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    host = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    time = models.DateTimeField(null=True)
    messages = models.CharField(max_length=255, blank=True)
    commandline = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return "{} - {} - {}".format(self.host, self.action, self.status)



