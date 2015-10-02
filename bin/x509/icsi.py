#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ICSI Notary lookup of FP 
#
# Software is free software released under the GNU General Public License version 3 and later
#
# Copyright (c) 2015 Alexandre Dulaunoy - a@foo.be


import dns.resolver
import argparse
import fileinput
import shlex
import redis

suffix = '.notary.icsi.berkeley.edu'

resolver = dns.resolver.Resolver()
fp = '592978A72A9061F70AD7C44C4D449DCF258CD534'

argParser = argparse.ArgumentParser(description='Lookup a series of certificate fingerprints ICSI Certificate Notary')
argParser.add_argument('-r', default='-', help='Read from a file, default is stdin')
args = argParser.parse_args()

icsi_keys = ['version','first_seen','last_seen', 'times_seen', 'validated']

rstore = redis.StrictRedis(host='localhost', port=6380, db=5)

for l in fileinput.input(args.r):
	fp = l.rstrip().lower()
	try:
		r = resolver.query(fp+suffix, 'TXT')
	except:
		print ("Non-existing certificate {}".format(fp))
		continue
	for rdata in r:
		txt = rdata.strings[0]
	rd = {}
	rd = dict(token.split('=') for token in shlex.split(txt))
	rstore.hmset(fp, rd)
	print (rd)
	#print ("{},{}".format(fp,r[0]))
