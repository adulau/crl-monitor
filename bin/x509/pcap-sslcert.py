#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tool to parse output of ssldump (not compiled with OpenSSL) to dump raw certificate
#
# Software is free software released under the GNU General Public License version 3 and later
#
# Copyright (c) 2015 Alexandre Dulaunoy - a@foo.be

import fileinput
import re
import binascii
import OpenSSL
import argparse

argParser = argparse.ArgumentParser(description='Extract certificate to PEM format from an ssldump output')
argParser.add_argument('-v', default=False, action='store_true', help='Verbose output')
argParser.add_argument('-r', default='-', help='Read from a file, default is stdin')
args = argParser.parse_args()

cert = None
certstring = ""

certtag = re.compile('^\s+Certificate\s*$')
certtagend = re.compile('^\S+')
ipv4re = '\d+\.\d+\.\d+\.\d+'
flowre = 'New TCP connection #(\d+): ('+ipv4re+')\(\d+\) <-> ('+ipv4re+')\((\d+)\)'
flow = re.compile(flowre)
for l in fileinput.input(args.r):
    if certtag.match(l):
        cert = True
        continue
    elif certtagend.match(l):
        cert = None
    if flow.search(l):
        m = flow.match(l)
        session = m.group(1)
        srcip = m.group(2)
        dstip = m.group(3)
        dstport = m.group(4)

    if (cert is True):
        certstring += l.rstrip('\n')

    if ((cert is None) and (len(certstring) > 0)):
        y = re.sub(" ", "", certstring).split('=')
        a = y[1].split('certificate')[0]
        dercert = binascii.unhexlify(a)
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, dercert)
        fp = x509.digest('sha1').replace(':','').lower()
        if args.v:
            print srcip+"<->"+dstip+":"+dstport
            print "Issuer: "+x509.get_issuer().CN
            print "CN: " + x509.get_subject().CN
        print OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, x509)
        certstring = ""
        y = ""
