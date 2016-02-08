#!/usr/bin/env python3

import os, sys, subprocess, datetime

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

if __name__ == '__main__':
    print(get_kernel())
    print(get_fqdn())
    print(get_uptime())
    print(get_date())
    print(get_ip_addr())
