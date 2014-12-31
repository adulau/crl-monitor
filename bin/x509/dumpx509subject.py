#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tool to dump DN from DER encoded X.509 certificate (in Base64)
#
# Software is free software released under the GNU General Public License version 3 and later
#
# Copyright (c) 2014 Alexandre Dulaunoy - a@foo.be

import fileinput
from M2Crypto import X509
import base64
import argparse
import redis
import sys

argParser = argparse.ArgumentParser(description='Dump DN from X.509 certificates')
argParser.add_argument('-c', action='store_true', default=True, help='Dump CSV')
argParser.add_argument('-s', action='store_true', default=False, help='Store in Redis')
argParser.add_argument('-b', default='127.0.0.1', help='Redis host (default is 127.0.0.1)')
argParser.add_argument('-p', default=6379, help='Redis TCP port (default is 6379)')
argParser.add_argument('-v', action='store_true', help='Verbose output')
argParser.add_argument('-r', default='-', help='Read from a file, default is stdin')
args = argParser.parse_args()

if args.s:
    try:
        #Redis structure Set of (Subject) per FP
        r = redis.StrictRedis(host=args.b, port=args.p)
    except:
        print "Unable to connect to the Redis server"
        sys.exit(1)

for cert in fileinput.input(args.r):
    try:
        fp = cert.split(",")[0]
        certb = base64.b64decode(cert.split(",")[1])
    except:
        if args.v:
            print "Padding error "+fileinput.lineno()
        pass

    try:
        x509 = X509.load_cert_string(certb, X509.FORMAT_DER)
    except:
        print "At line number "+ str(fileinput.lineno()) + " parsing error"
        pass
    subject = x509.get_subject().as_text()
    if subject is not None:
        if not args.s:
            print fp +","+ subject
        elif args.s:
            r.sadd(fp, subject)
        else:
            sys.exit(1)


