#!/usr/bin/env python

from __future__ import print_function
import subprocess
import threading

def is_reacheable(ip):
    
    if subprocess.call('ping -w3 -c1 ' + ip + '| grep received | awk -F" " \'{print $4 }\'', shell=True, stdout=subprocess.PIPE):

        print("{0} is unreacheable".format(ip))
    else:
        print("{0} is alive".format(ip))        

def main():
    with open('references/ip.list') as f:
        lines = f.readlines()
        threads = []
        for line in lines:
            thr = threading.Thread(target=is_reacheable, args=(line,))
            thr.start()
            threads.append(thr)

        for thr in threads:
            thr.join()

if __name__ == '__main__':
    main()
