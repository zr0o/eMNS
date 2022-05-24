####################################################################################
### Bipul Ghimire
### email : thebipul79@gmail.com
#####################################################################################
from import_export import resources
from .models import Device
from .models import Log

class DeviceResource(resources.ModelResource):
    class Meta:
        model = Device

class LogResource(resources.ModelResource):
    class Meta:
        model = Log