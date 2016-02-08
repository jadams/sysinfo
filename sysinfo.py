#!/usr/bin/env python3

import os, sys, subprocess, datetime

def pretty_print(kernel=True, fqdn=True, uptime=True, date=True, ipaddr=True, iproute=True):
    print('Kernel: {0} release: {1}'.format(*get_kernel()))
    print('Hostname: {0}.{1}.{2}'.format(*get_fqdn()))
    print('Uptime: {days} Days, {hours} Hours, {mins} Minutes'.format(**get_uptime()))

def get_kernel():
    kernel =  subprocess.check_output(['uname', '-r']).decode('utf-8').strip('\n')
    kernel = kernel.split('-')
    return kernel


def get_fqdn():
    fqdn = subprocess.check_output(['hostname', '-f']).decode('utf-8').strip('\n')
    fqdn = fqdn.split('.')
    return fqdn

def get_uptime():
    uptime = subprocess.check_output(['uptime', '-p']).decode('utf-8').strip('\n')
    uptime = uptime.replace(',', '')
    uptime = uptime.split()
    return {'days':int(uptime[1]), 'hours':int(uptime[3]), 'mins':int(uptime[5])}

def get_date():
    dt = str(datetime.datetime.now()).split()
    dt[1] = dt[1].split('.')[0]
    return dt

def get_ip_addr():
    addr = subprocess.check_output(['ip', 'addr']).decode('utf-8').strip('\n')
    addr = addr.split('\n')
    ip = {}
    for line in addr:
        if line[0].isdigit():
            iface = line.split()[1].strip(':')
            ip[iface] = {'ipv6':[], 'ipv4':[]}
        if 'inet6' in line:
            address = line.split()[1].split('/')
            ip[iface]['ipv6'].append(address)
        elif 'inet' in line:
            address = line.split()[1].split('/')
            ip[iface]['ipv4'].append(address)
    return ip

def get_ip_route():
    route = subprocess.check_output(['ip', 'route']).decode('utf-8').strip('\n')
    route = route.split('\n')
    routes = {}
    for line in route:
        info = line.split()
        name = info[0]
        routes[name] = {}
        for i in range(1,len(info)):
            if info[i] == 'dev':
                routes[name]['dev'] = info[i+1]
            elif info[i] == 'via':
                routes[name]['via'] = info[i+1]
            elif info[i] == 'src':
                routes[name]['src'] = info[i+1]
    return routes

if __name__ == '__main__':
    #print(get_kernel())
    #print(get_fqdn())
    #print(get_uptime())
    #print(get_date())
    #print(get_ip_addr())
    #print(get_ip_route())
    pretty_print()
