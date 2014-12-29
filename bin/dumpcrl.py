#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tool to dump CRL and OCSP URI from DER encoded X.509 certificate (in Base64)
#
# Software is free software released under the GNU General Public License version 3 and later
#
# Copyright (c) 2014 Alexandre Dulaunoy - a@foo.be

import fileinput
from M2Crypto import X509
import base64
import magic
import argparse
import json

argParser = argparse.ArgumentParser(description='Dump CRL URI and OCSP URI from X.509 certificates')
argParser.add_argument('-j', action='store_true', default=False, help='Dump JSON')
argParser.add_argument('-c', action='store_true', default=True, help='Dump CSV')
argParser.add_argument('-v', action='store_true', help='Verbose output')
argParser.add_argument('-r', default='-', help='Read from a file, default is stdin')
args = argParser.parse_args()

def mapExtension(ext=None):
    if ext is None:
        return False
    return dict([v.strip().split(':', 1) for v in ext.split('\n') if v.strip()])

def certValues(cert=None):
    if cert is None:
        return False

for cert in fileinput.input(args.r):
    try:
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
    #print x509.get_subject().as_text()
    # CRL
    try:
        crlExt = x509.get_ext('crlDistributionPoints').get_value()
        crlExts = mapExtension(ext=crlExt)
        if args.j:
            print json.dumps(crlExts)
        elif args.c:
            print "CRL URI," + crlExts['URI']
    except:
        if args.v:
            print "No CRL for " + str(fileinput.lineno())
        pass

    # OCSP
    try:
        ocspExt = x509.get_ext('authorityInfoAccess').get_value()
        ocspExts = mapExtension(ext=ocspExt)
        if args.j:
            print json.dumps(ocspExts)
        elif args.c:
            print "OCSP URI," + str(ocspExts['OCSP - URI'])
            print "CA Issuers - URI," + str(ocspExts['CA Issuers - URI'])
    except:
        if args.v:
            print "No OCSP for " + str(fileinput.lineno())
        pass

