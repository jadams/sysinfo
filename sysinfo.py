#!/usr/bin/env python3

import os, sys, subprocess, datetime

def _get_kernel():
    kernel =  subprocess.check_output(['uname', '-r']).decode('utf-8').strip('\n')
    kernel = kernel.split('-')
    return kernel

def _get_fqdn():
    fqdn = subprocess.check_output(['hostname', '-f']).decode('utf-8').strip('\n')
    fqdn = fqdn.split('.')
    return fqdn

def _get_uptime():
    uptime = subprocess.check_output(['uptime', '-p']).decode('utf-8').strip('\n')
    uptime = uptime.replace(',', '')
    uptime = uptime.split()
    return {'days':int(uptime[1]), 'hours':int(uptime[3]), 'mins':int(uptime[5])}

def _get_date():
    dt = str(datetime.datetime.now()).split()
    dt[1] = dt[1].split('.')[0]
    return dt

def _get_ip_addr():
    addr = subprocess.check_output(['ip', 'addr']).decode('utf-8').strip('\n')
    addr = addr.split('\n')
    addrs = {}
    for line in addr:
        if line[0].isdigit():
            iface = line.split()[1].strip(':')
            addrs[iface] = {'ipv6':[], 'ipv4':[]}
        if 'inet6' in line:
            address = line.split()[1].split('/')
            addrs[iface]['ipv6'].append(address)
        elif 'inet' in line:
            address = line.split()[1].split('/')
            addrs[iface]['ipv4'].append(address)
    return addrs

def _get_ip_route():
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

def _get_users():
    if not os.path.isfile('/etc/passwd'):
        return NULL
    else:
        users = {}
        try:
            with open('/etc/passwd', 'r') as passwd:
                for line in passwd:
                    line = line.strip('\n').split(':')
                    if int(line[2]) >= 1000:
                        users[line[0]] = {'uid':int(line[2]), 'gid':int(line[3]), 'home':line[5], 'shell':line[6]}
        except:
            return NULL
        return users

def _detect_distro():
    if os.path.isfile('/etc/os-release'):
        with open('/etc/os-release', 'r') as relfile:
            ddict = {}
            for line in relfile:
                ll = line.strip('\n').replace('\"', '').split('=')
                if len(ll) > 1:
                    ddict[ll[0].lower()] = ll[1]
        return ddict
    else:
        try:
            subprocess.check_output(['lsb_release', '-a'])
        except:
            if os.path.isfile('/etc/redhat-release'):
                return {'id':'Redhat Linux'}
            elif os.path.isfile('/etc/debian_version'):
                return {'id':'Debian Linux'}
            else:
                return {'id':'Other Linux'}

def _get_processes():
    return

def _get_hosts():
    return

def _get_dns():
    return

def _get_mounts():
    return

def _get_cpuinfo():
    if os.path.isfile('/proc/cpuinfo'):
        with open('/proc/cpuinfo', 'r') as cpuinfo:
            for line in cpuinfo:
                if 'model name' in line:
                    return line.strip('\n').split(':')[1].split()

def _get_meminfo():
    meminfo = subprocess.check_output(['free', '-h']).decode('utf-8').strip('\n').split()
    return {'total':meminfo[7], 'used':meminfo[8], 'swap':meminfo[14]}

def _get_current_user():
    return os.getenv('USER')

def _get_systemd_services():
    return

def _get_initd_services():
    return

def _get_usb_dev():
    return

def _get_pci_dev():
    return

def _get_listening_ports():
    return

def full_print(kernel=True, fqdn=True, uptime=True, date=True, ipaddr=True, iproute=True):
    print('Kernel:\t{0}-{1}'.format(*_get_kernel()))
    print('Host:\t{0}.{1}.{2}'.format(*_get_fqdn()))
    print('Uptime:\t{days} Days, {hours} Hours, {mins} Minutes'.format(**_get_uptime()))
    print('Date:\t{0} {1}'.format(*_get_date()))

    print('IP Addresses: ')
    ipinfo = _get_ip_addr()
    for iface in ipinfo:
        print('{}:'.format(iface))
        if not ipinfo[iface]['ipv4']:
            continue
        else:
            print('\tIPv4:')
            for addr in ipinfo[iface]['ipv4']:
                print('\t\t{}'.format('/'.join(addr)))
        if not ipinfo[iface]['ipv6']:
            continue
        else:
            print('\tIPv6:')
            for addr in ipinfo[iface]['ipv6']:
                print('\t\t{}'.format('/'.join(addr)))

    print('Routes:')
    iproute = _get_ip_route()
    for route in iproute:
        proute = '\t{}'.format(route)
        for key in iproute[route]:
            #proute = proute+' '+key+' '+iproute[route][key] 
            proute = '{0} {1} {2}'.format(proute, key, iproute[route][key]) 
        print(proute)

    print('Users:')
    users = _get_users()
    for user in users:
        print('\t{0}: {1}'.format(user, 'uid={uid}, gid={gid}, home={home}, shell={shell}'.format(**users[user])))

    print('CPU:\t{}'.format(' '.join(_get_cpuinfo())))
    print('Memory:\t{total}/{used} Swap: {swap}'.format(**_get_meminfo()))

def short_print():
    print('{0} {1}'.format(*_get_date()))
    print('{0}@{1}'.format(_get_current_user(), _get_fqdn()[0]))
    print('{0}-{1}'.format(*_get_kernel()))
    print('Up: {days} Days, {hours} Hours, {mins} Minutes'.format(**_get_uptime()))

if __name__ == '__main__':
    full_print()
    #short_print()
