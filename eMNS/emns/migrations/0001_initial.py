# Generated by Django 4.0.3 on 2022-04-04 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=True, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(help_text='xxx.xxx.xxx.xxx')),
                ('subnetmask', models.GenericIPAddressField(help_text='000.000.000.000')),
                ('hostname', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(blank=True, max_length=255)),
                ('position', models.CharField(blank=True, max_length=255)),
                ('location', models.CharField(blank=True, max_length=255)),
                ('sshport', models.IntegerField(default=22)),
                ('vendor_type', models.CharField(choices=[('cisco', 'Cisco'), ('mikrotik', 'MikroTik'), ('juniper', 'Juniper')], max_length=255)),
                ('device_type', models.CharField(choices=[('router', 'Router'), ('switch', 'Switch')], max_length=255)),
                ('device_series', models.CharField(choices=[('Cisco Industrial Ethernet 2000 Switches', 'Cisco Industrial Ethernet 2000 Switches'), ('Cisco Industrial Ethernet 3000 Switches', 'Cisco Industrial Ethernet 3000 Switches'), ('Cisco Industrial Ethernet 4000 Switches', 'Cisco Industrial Ethernet 4000 Switches'), ('Cisco Industrial Ethernet 5000 Switches', 'Cisco Industrial Ethernet 5000 Switches'), ('Cisco Switch Catalyst 4500', 'Cisco Switch Catalyst 4500'), ('Cisco Switch Catalyst 4900', 'Cisco Switch Catalyst 4900'), ('Cisco Switch Catalyst 6800', 'Cisco Switch Catalyst 6800'), ('Cisco Switch Catalyst 3560', 'Cisco Switch Catalyst 3560'), ('Cisco Switch Catalyst 3750', 'Cisco Switch Catalyst 3750'), ('Cisco Switch Catalyst 6500', 'Cisco Switch Catalyst 6500'), ('Switch Catalyst 100', 'Mikrotik Switch Catalyst 100'), ('Cisco Router ISR 1900', 'Juniper Router ISR 1900'), ('Cisco Router ISR 2900', 'Cisco Router ISR 2900'), ('Cisco Router ISR 3900', 'Cisco Router ISR 3900'), ('Cisco Router ISR 4000', 'Cisco Router ISR 4000'), ('Cisco Router ISR 1100', 'Cisco Router ISR 1100'), ('Cisco Router ISR 800', 'Cisco Router ISR 800'), ('Cisco Router ISR 900', 'Cisco Router ISR 900'), ('Cisco Router ASR 900', 'Cisco Router ASR 900'), ('Cisco Router ASR 1000', 'Cisco Router ASR 1000'), ('Cisco Router ASR 5000', 'Cisco Router ASR 5000'), ('Cisco Router ASR 9000', 'Cisco Router ASR 9000'), ('Cisco 8000 Series Routers', 'Cisco 8000 Series Routers'), ('Cisco Router 10000 Series', 'Cisco Router 10000 Series'), ('Cisco Router 12000 Series', 'Cisco Router 12000 Series'), ('Cisco Router ISR 1800', 'Cisco Router ISR 1800'), ('Cisco Router ISR 2800', 'Cisco Router ISR 2800'), ('Cisco Router ISR 3800', 'Cisco Router ISR 3800'), ('Cisco Router 7200 Series', 'Cisco Router 7200 Series'), ('Cisco Router 7600 Series', 'Cisco Router 7600 Series'), ('Juniper Router', 'Juniper Router')], max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=255)),
                ('action', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('time', models.DateTimeField(null=True)),
                ('messages', models.CharField(blank=True, max_length=255)),
                ('commandline', models.CharField(blank=True, max_length=1000)),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emns.device')),
            ],
        ),
    ]