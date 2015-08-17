#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Lookup IP for known fingerprints and X.509 subjects via HTTP API
#
# Software is free software released under the GNU General Public License version 3 and later
#
# Copyright (c) 2015 Alexandre Dulaunoy - a@foo.be

import redis
import sys
import netaddr
import json
import re

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)
ipmaxsize = 512 #/23

class SSLQueryHandler(tornado.web.RequestHandler):

    def get(self, input):
        try:
            #Redis structure Set of (FP) per IP
            r = redis.StrictRedis(host='127.0.0.1', port=8323)
        except:
            print "Unable to connect to the Redis server"
            sys.exit(255)
        subnets = [input]
        out = {}
        for subnet in subnets:
            if re.findall(r":", subnet):
                self.clear()
                self.set_status(400)
                self.finish('IPv6 is not (yet) supported')
                continue
            try:
                iplist = netaddr.IPNetwork(subnet)
            except:
                self.clear()
                self.set_status(400)
                self.finish('Incorrect format')
                continue

            if iplist.size > ipmaxsize:
                self.clear()
                self.set_status(400)
                self.finish('Maximum CIDR block size reached >/23')

                if not self._finished:
                    self.finish()
            for ip in iplist:
                s = r.smembers(ip)
                if s:
                    out[str(ip)] = {}
		    out[str(ip)]['certificates'] = []
	            out[str(ip)]['subjects'] = {}
                    for fingerprint in s:
                        subjects = r.smembers(fingerprint)
			out[str(ip)]['certificates'].append(fingerprint)
                        if subjects:
			    out[str(ip)]['subjects'][fingerprint] = {}
			    out[str(ip)]['subjects'][fingerprint]['values'] = []
                            for subject in subjects:
                                    out[str(ip)]['subjects'][fingerprint]['values'].append(subject)

        if not self._finished:
            self.set_header('Content-Type', 'application/json')
            self.set_header('Server', 'https://github.com/adulau/crl-monitor')
            self.write(json.dumps(out))


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
        (r"/query/(.*)", SSLQueryHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

