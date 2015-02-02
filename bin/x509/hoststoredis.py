#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tool to dump IP,set(FP) and FP,set(IP) into a Redis database
#
# Software is free software released under the GNU General Public License version 3 and later
#
# Copyright (c) 2015 Alexandre Dulaunoy - a@foo.be

import fileinput
import argparse
import redis
import sys

argParser = argparse.ArgumentParser(description='Tool to dump IP,FP into Redis')
argParser.add_argument('-s', action='store_true', default=True, help='Store in Redis')
argParser.add_argument('-b', default='127.0.0.1', help='Redis host (default is 127.0.0.1)')
argParser.add_argument('-p', default=6379, help='Redis TCP port (default is 6379)')
argParser.add_argument('-v', action='store_true', help='Verbose output')
argParser.add_argument('-r', default='-', help='Read from a file, default is stdin')
args = argParser.parse_args()

if args.s:
    try:
        r = redis.StrictRedis(host=args.b, port=args.p)
    except:
        print "Unable to connect to the Redis server"
        sys.exit(1)

for l in fileinput.input(args.r):
    (ip, fp) = l.split(',')
    if args.s:
        cfp = fp.rstrip()
        r.sadd(ip, cfp)
        r.sadd("s:"+cfp, ip)
    else:
        sys.exit(1)
