#!/usr/bin/env python3

import os, sys, subprocess

def get_kernel():
    kernel =  subprocess.check_output(['uname', '-r']).decode('utf-8').strip('\n')
    kernel = kernel.split('-')
    return kernel

if __name__ == '__main__':
    print(get_kernel())
    print
