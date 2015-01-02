#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Lookup IP for known fingerprints and X.509 subjects
#
# Software is free software released under the GNU General Public License version 3 and later
#
# Copyright (c) 2015 Alexandre Dulaunoy - a@foo.be

import fileinput
import argparse
import redis
import sys
import netaddr

argParser = argparse.ArgumentParser(description='Tool to lookup IP for known fingerprints and X.509 subjects')
argParser.add_argument('-b', default='127.0.0.1', help='Redis host (default is 127.0.0.1)')
argParser.add_argument('-p', default=6379, help='Redis TCP port (default is 6379)')
argParser.add_argument('-s', action='append', help='IPv4 subnet to lookup')
argParser.add_argument('-v', action='store_true', help='Verbose output')
args = argParser.parse_args()

if args.s is None:
    sys.exit(255)

try:
    #Redis structure Set of (FP) per IP
    r = redis.StrictRedis(host=args.b, port=args.p)
except:
    print "Unable to connect to the Redis server"
    sys.exit(1)

for subnet in args.s:
    iplist = netaddr.IPNetwork(subnet)
    for ip in iplist:
        s = r.smembers(ip)
        if s:
            print ip
            for x in s:
                subjects = r.smembers(x)
                if subjects:
                    for subject in subjects:
                        print " " + subject
                else:
                    print " " + x
