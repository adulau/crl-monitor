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
import json

argParser = argparse.ArgumentParser(description='Tool to lookup IP for known fingerprints and X.509 subjects')
argParser.add_argument('-b', default='127.0.0.1', help='Redis host (default is 127.0.0.1)')
argParser.add_argument('-p', default=6379, help='Redis TCP port (default is 6379)')
argParser.add_argument('-s', action='append', help='IPv4 subnet to lookup')
argParser.add_argument('-v', action='store_true', help='Verbose output')
argParser.add_argument('-o', default='readable', help='readable (default), json')
args = argParser.parse_args()

if args.s is None:
    sys.exit(255)

try:
    #Redis structure Set of (FP) per IP
    r = redis.StrictRedis(host=args.b, port=args.p)
except:
    print "Unable to connect to the Redis server"
    sys.exit(255)

if args.o == 'json':
    out = {}
elif args.o == 'readable':
    pass
else:
    print "Unknown output format"
    sys.exit(255)

for subnet in args.s:
    iplist = netaddr.IPNetwork(subnet)
    for ip in iplist:
        s = r.smembers(ip)
        if s:
            if args.o == 'readable':
                print ip
            else:
                out[str(ip)] = []
            for fingerprint in s:
                subjects = r.smembers(fingerprint)
                if subjects:
                    for subject in subjects:
                        if args.o == 'readable':
                            print " " + subject
                        else:
                            out[str(ip)].append(subject)
                else:
                    if args.o == 'readable':
                        print " " + fingerprint
                    else:
                        out[str(ip)].append(fingerprint)

if args.o == 'json':
    print json.dumps(out)
