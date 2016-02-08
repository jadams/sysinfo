#!/usr/bin/env python3

import os, sys, subprocess

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
    return uptime

if __name__ == '__main__':
    print(get_kernel())
    print(get_fqdn())
    print(get_uptime())
