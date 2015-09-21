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

suffix = '.notary.icsi.berkeley.edu'

resolver = dns.resolver.Resolver()
fp = '592978A72A9061F70AD7C44C4D449DCF258CD534'

argParser = argparse.ArgumentParser(description='Lookup a series of certificate fingerprints ICSI Certificate Notary')
argParser.add_argument('-r', default='-', help='Read from a file, default is stdin')
args = argParser.parse_args()

for l in fileinput.input(args.r):
	fp = l.rstrip()
	try:
		r = resolver.query(fp+suffix, 'TXT')[0]
	except:
		print ("Non-existing certificate {}".format(fp))
		continue
	print ("{},{}".format(fp,r))
