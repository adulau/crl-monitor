#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Analyze CRLs stored in a directory and dump a JSON
#
# Software is free software released under the GNU General Public License version 3 and later
#
# Copyright (c) 2014 Alexandre Dulaunoy - a@foo.be

import argparse
import sys
import os
from pyasn1_modules import rfc2459
crlspec = rfc2459.CertificateList()
from pyasn1.codec.der import decoder
import OpenSSL
import json
import binascii
import datetime

argParser = argparse.ArgumentParser(description='Analyze CRLs stored in a directory')
argParser.add_argument('-v', action='store_true', help='Verbose output')
argParser.add_argument('-d', help='Path where CRLs are stored')
argParser.add_argument('-j', action='store_false', default=True, help='Toggle JSON output (default)')
args = argParser.parse_args()

if not args.d:
    argParser.print_help()
    sys.exit()

def DNToString(dn):
  ret = ""
  for x in dn:
    for y in x:
        ret = ret + " " + str(y[0][1])
  return ret

for crl in os.listdir(args.d):
    crlpath = os.path.join(args.d,crl)
    f = open(crlpath, 'rb')
    crlfile = f.read()
    try:
        crlp = OpenSSL.crypto.load_crl(OpenSSL.crypto.FILETYPE_ASN1, crlfile)
    except Exception, err:
        if args.v:
            print err
        continue

    fx = open(crlpath, 'rb')
    crlfileasn = fx.read()
    try:
        cert, rest = decoder.decode(crlfileasn, asn1Spec=crlspec)
    except Exception, err:
        if args.v:
            print err
        continue
    a = cert['tbsCertList']
    if a.getComponentByName('thisUpdate') is not None:
        thisUpdate = str(a.getComponentByName('thisUpdate')[0])
    else:
        thisUpdate = None
    if a.getComponentByName('nextUpdate') is not None:
        nextUpdate = str(a.getComponentByName('nextUpdate')[0])
    else:
        nextUpdate = None
    issuer = DNToString(a.getComponentByName('issuer'))
    fx.close()

    if crlp.get_revoked() is None:
        o = {'crlpath': crlpath, 'revoked': None, 'issuer' : issuer, 'thisUpdate': thisUpdate, 'nextUpdate': nextUpdate}
    else:
        o = {'crlpath': crlpath, 'revoked': [], 'issuer' : issuer, 'thisUpdate': thisUpdate, 'nextUpdate': nextUpdate}
        for revoked in crlp.get_revoked():
            o['revoked'].append({'serial':revoked.get_serial(), 'rev_date':revoked.get_rev_date(), 'reason':revoked.get_reason()})
    if args.j:
        print json.dumps(o)
