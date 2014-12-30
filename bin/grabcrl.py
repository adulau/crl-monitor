#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Grab and Store CRL.
#
# Software is free software released under the GNU General Public License version 3 and later
#
# Copyright (c) 2014 Alexandre Dulaunoy - a@foo.be

import fileinput
import argparse
import requests
import os
import datetime
import hashlib

argParser = argparse.ArgumentParser(description='Grab and Store CRL')
argParser.add_argument('-v', action='store_true', help='Verbose output')
argParser.add_argument('-r', default='-', help='Read CRL list from a file, default is stdin')
argParser.add_argument('-d', default='../crls/', help='Path to store CRL')
args = argParser.parse_args()

if not os.path.exists(args.d):
    os.makedirs(args.d)

currentdate = datetime.datetime.now().strftime('%Y/%m/%d')

d = args.d
for dirname in currentdate.split('/'):
    d = os.path.join(d,dirname)
    if not os.path.exists(d):
        os.makedirs(d)

storepath = d

for url in fileinput.input(args.r):
    headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' }
    hurl = hashlib.sha256(url.rstrip()).hexdigest()
    try:
        if args.v:
            print "Fetching..." + url.rstrip()
        r = requests.get(url.rstrip(), headers=headers, timeout=2)
        if args.v:
            print url.rstrip() + " HTTP status code " + str(r.status_code) + " for linenumber " + str(fileinput.lineno())
    except Exception, err:
        if args.v:
            print err
            continue
    if r.status_code >= 200 and r.status_code <= 299:
        with open (os.path.join(storepath,hurl), 'w') as f:
            f.write(r.content)
