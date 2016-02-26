#!/usr/bin/env python3

# Copyright (c) 2016 John Adams <john@hexb.it> & Tom Carrio <tom@carrio.me>
# Terrible coding is standard practice
# Let me know what I can do better by emailing me at <sysinfo@hexb.it> or
#  by submitting a pull request at (https://github.com/jadams/sysinfo)

import os, sys, subprocess, datetime, json

def _get_kernel():
    kernel =  subprocess.check_output(['uname', '-r']).decode('utf-8').strip('\n')
    kernel = kernel.split('-')
    return kernel

def _get_fqdn():
    fqdn = subprocess.check_output(['hostname', '-f']).decode('utf-8').strip('\n')
    fqdn = fqdn.split('.')
    return fqdn

def _get_uptime():
    with open('/proc/uptime', 'r') as upfile:
        uptime = datetime.timedelta(seconds = float(upfile.readline().split()[0]))
    return {'days':uptime.days, 'hours':int(uptime.seconds/3600), 'mins':int(uptime.seconds%3600/60), 'secs':int(uptime.seconds%3600%60)}

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
    try:
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
    except:
        return 

def _get_users():
    if not os.path.isfile('/etc/passwd'):
        return
    else:
        users = {}
        try:
            with open('/etc/passwd', 'r') as passwd:
                for line in passwd:
                    line = line.strip('\n').split(':')
                    if int(line[2]) >= 1000 and int(line[2]) < 65534:
                        users[line[0]] = {'uid':int(line[2]),
                                          'gid':int(line[3]),
                                          'home':line[5],
                                          'shell':line[6]}
        except:
            return
        return users

def _get_disks():
    try:
        ddisks = {}
        df_keys=['filesystem','size','used','avail','use%','mount']
        df = subprocess.check_output(['df', '-h']).decode('utf-8')[:-1].split('\n')
        mounts = subprocess.check_output('mount').decode('utf-8')[:-1].split('\n')
        
        # pull info from 'df -h'
        for line in df:
            if('/'==line[0]):
                line=line.split()
                ddisks.update({line[5]:dict()})
                for i in range(0,5):
                    ddisks[line[5]][df_keys[i]]=line[i]

        # pull info from mount using new df dict
        for m in mounts:
            for d in ddisks:
                m_info = m.split()
                if(m_info[2]==d):
                    ddisks[d]['type']=m_info[4]
                    ddisks[d]['permission']=m_info[5].split(',')[0][1:]
        return ddisks
    except:
        return

def _detect_distro():
    return

def _get_processes():
    pdict = {'_total':len([c for c in subprocess.check_output(['ps','aux']) if('\n'==c)])-1}
    pdict.update({'users':{}})
    [pdict.update({'users':{u:len([c for c in subprocess.check_output(['ps','-u',u]) if('\n'==c)])-1}}) for u in _get_users()]
    return pdict

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
    mem = meminfo.index("Mem:")
    swap = meminfo.index("Swap:")
    return {'total':meminfo[int(mem)+1],
            'used':meminfo[int(mem)+2],
            'swap_total':meminfo[int(swap)+1],
            'swap_used':meminfo[int(swap)+2]}

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

def full_print():
    print('Kernel:\t{0}-{1}'.format(*_get_kernel()))
    print('Host:\t{}'.format('.'.join(_get_fqdn())))
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
    if iproute:
        for route in iproute:
            proute = '\t{}'.format(route)
            for key in iproute[route]:
                #proute = proute+' '+key+' '+iproute[route][key]
                proute = '{0} {1} {2}'.format(proute, key, iproute[route][key])
            print(proute)

    print('Users:')
    users = _get_users()
    for user in users:
        print('\t{0}: {1}'.format(user,
            'uid={uid}, gid={gid}, home={home}, shell={shell}'.format(**users[user])))

    print('CPU:\t{}'.format(' '.join(_get_cpuinfo())))
    print('Memory:\t{used}/{total} Swap: {swap_used}/{swap_total}'.format(**_get_meminfo()))

    print('Processes:')
    processes=_get_processes()
    if(processes):
        for username in processes['users']:
            print('\t{0}: {1}'.format(username,processes['users'][username]))
        print('\t{0}: {1}'.format('Total',processes['_total']))

    print('Disks:')
    _disk_dict = _get_disks()
    for disk in _disk_dict:
        disk_info='\t\tMount:{0}, Type:{type}, Permission:{permission},\n\t\tSize:{size}, Avail:{avail}, Used%:{use%}'.format(disk,**_disk_dict[disk])
        print('\t{}:\n{}'.format(_disk_dict[disk]['filesystem'],disk_info))


def short_print():
    print(' '.join(_get_date()))
    print('{0}@{1}'.format(_get_current_user(), _get_fqdn()[0]))
    print('-'.join(_get_kernel()))
    print('Up: {days} Days, {hours} Hours, {mins} Minutes'.format(**_get_uptime()))

def get_json():
    jdb = {}
    jdb['kernel'] = _get_kernel()
    jdb['hostname'] = _get_fqdn()
    jdb['uptime'] = _get_uptime()
    jdb['date'] = _get_date()
    jdb['ipaddr'] = _get_ip_addr()
    jdb['iproute'] = _get_ip_route()
    jdb['users'] = _get_users()
    jdb['cpu'] = _get_cpuinfo()
    jdb['mem'] = _get_meminfo()
    return jdb

if __name__ == '__main__':
    full_print()
    print('==============================')
    short_print()
    with open('host.json', 'w') as outfile:
        json.dump(get_json(), outfile)