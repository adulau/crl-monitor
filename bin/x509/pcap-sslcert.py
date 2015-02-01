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

cert = None
certstring = ""

certtag = re.compile('^\s+Certificate\s*$')
certtagend = re.compile('^\S+')

for l in fileinput.input():
    if certtag.match(l):
        cert = True
        continue
    elif certtagend.match(l):
        cert = None

    if (cert is True):
        certstring += l.rstrip('\n')

    if ((cert is None) and (len(certstring) > 0)):
        y = re.sub(" ", "", certstring).split('=')
        a = y[1].split('certificate')[0]
        dercert = binascii.unhexlify(a)
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, dercert)
        fp = x509.digest('sha1').replace(':','').lower()
        print OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, x509)
        certstring = ""
        y = ""
